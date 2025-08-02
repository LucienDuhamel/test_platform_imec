def cnfg_master_spi(AxiQspi, clk_phase=0, clk_pol=0):
    print("Configure device")
    # Reset the SPI device
    AxiQspi.write(XSP_SRR_OFFSET, XSP_SRR_RESET_MASK)
    # Enable the transmit empty interrupt, which we use to determine progress on the transmission. 
    AxiQspi.write(XSP_IIER_OFFSET, XSP_SR_TX_EMPTY_MASK)
    # Disable the global IPIF interrupt
    AxiQspi.write(XSP_DGIER_OFFSET, 0)
    # Deselect the slave on the SPI bus
    AxiQspi.write(XSP_SSR_OFFSET, SLAVE_NO_SELECTION)
    # Disable the transmitter, enable Manual Slave Select Assertion, put SPI controller into master mode, and enable it
    ControlReg = AxiQspi.read(XSP_CR_OFFSET)
    ControlReg = ControlReg | XSP_CR_MASTER_MODE_MASK | XSP_CR_MANUAL_SS_MASK | XSP_CR_ENABLE_MASK | XSP_CR_TXFIFO_RESET_MASK | XSP_CR_RXFIFO_RESET_MASK
    AxiQspi.write(XSP_CR_OFFSET, ControlReg)
    ControlReg = AxiQspi.read(XSP_CR_OFFSET)
    ControlReg = ControlReg & ~(XSP_CR_CLK_PHASE_MASK | XSP_CR_CLK_POLARITY_MASK) 
    if clk_phase == 1:
        ControlReg = ControlReg | XSP_CR_CLK_PHASE_MASK
    if clk_pol == 1:
        ControlReg = ControlReg | XSP_CR_CLK_POLARITY_MASK
    AxiQspi.write(XSP_CR_OFFSET, ControlReg)

    return 0

def xfer(AxiQspi, packet):
    # print("TransferData")
    for data in packet:
        AxiQspi.write(XSP_SSR_OFFSET, 0xFFFFFFFE)
        AxiQspi.write(XSP_DTR_OFFSET, data)
        ControlReg = AxiQspi.read(XSP_CR_OFFSET)
        ControlReg = ControlReg & ~XSP_CR_TRANS_INHIBIT_MASK
        AxiQspi.write(XSP_CR_OFFSET, ControlReg)

        StatusReg = AxiQspi.read(XSP_SR_OFFSET)
        while (StatusReg & XSP_SR_TX_EMPTY_MASK) == 0:
            StatusReg = AxiQspi.read(XSP_SR_OFFSET)
        
        # DEBUG
        # print('XSP_RFO_OFFSET  : 0x{0:08x}'.format(AxiQspi.read(XSP_RFO_OFFSET)))
        ControlReg = AxiQspi.read(XSP_CR_OFFSET)
        ControlReg = ControlReg | XSP_CR_TRANS_INHIBIT_MASK
        AxiQspi.write(XSP_CR_OFFSET, ControlReg)

    AxiQspi.write(XSP_SSR_OFFSET, SLAVE_NO_SELECTION)

    # print("ReadResponse")
    resp = []
    RxFifoStatus = AxiQspi.read(XSP_SR_OFFSET) & 0x01
    while RxFifoStatus == 0:
        temp = AxiQspi.read(XSP_RFO_OFFSET)
        # DEBUG
        # print('XSP_RFO_OFFSET  : 0x{0:08x}'.format(temp))
        temp = AxiQspi.read(XSP_DRR_OFFSET)
        # DEBUG
        # print('XSP_DRR_OFFSET  : 0x{0:02x}'.format(temp)) 
        
        resp.append(temp)
        RxFifoStatus = AxiQspi.read(XSP_SR_OFFSET) & 0x01

    return resp