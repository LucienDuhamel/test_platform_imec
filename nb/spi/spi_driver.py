from . import spi_pkg


def cnfg_master_spi(AxiQspi, clk_phase=0, clk_pol=0):
    print("Configure device")
    # Reset the SPI device
    AxiQspi.write(spi_pkg.XSP_SRR_OFFSET, spi_pkg.XSP_SRR_RESET_MASK)
    # Enable the transmit empty interrupt, which we use to determine progress on the transmission. 
    AxiQspi.write(spi_pkg.XSP_IIER_OFFSET, spi_pkg.XSP_SR_TX_EMPTY_MASK)
    # Disable the global IPIF interrupt
    AxiQspi.write(spi_pkg.XSP_DGIER_OFFSET, 0)
    # Deselect the slave on the SPI bus
    AxiQspi.write(spi_pkg.XSP_SSR_OFFSET, spi_pkg.SLAVE_NO_SELECTION)
    # Disable the transmitter, enable Manual Slave Select Assertion, put SPI controller into master mode, and enable it
    ControlReg = AxiQspi.read(spi_pkg.XSP_CR_OFFSET)
    ControlReg = ControlReg | spi_pkg.XSP_CR_MASTER_MODE_MASK | spi_pkg.XSP_CR_MANUAL_SS_MASK | spi_pkg.XSP_CR_ENABLE_MASK | spi_pkg.XSP_CR_TXFIFO_RESET_MASK | spi_pkg.XSP_CR_RXFIFO_RESET_MASK
    AxiQspi.write(spi_pkg.XSP_CR_OFFSET, ControlReg)
    ControlReg = AxiQspi.read(spi_pkg.XSP_CR_OFFSET)
    ControlReg = ControlReg & ~(spi_pkg.XSP_CR_CLK_PHASE_MASK | spi_pkg.XSP_CR_CLK_POLARITY_MASK) 
    if clk_phase == 1:
        ControlReg = ControlReg | spi_pkg.XSP_CR_CLK_PHASE_MASK
    if clk_pol == 1:
        ControlReg = ControlReg | spi_pkg.XSP_CR_CLK_POLARITY_MASK
    AxiQspi.write(spi_pkg.XSP_CR_OFFSET, ControlReg)

    return 0

def xfer(AxiQspi, packet):
    # print("TransferData")
    for data in packet:
        AxiQspi.write(spi_pkg.XSP_SSR_OFFSET, 0xFFFFFFFE)
        AxiQspi.write(spi_pkg.XSP_DTR_OFFSET, data)
        ControlReg = AxiQspi.read(spi_pkg.XSP_CR_OFFSET)
        ControlReg = ControlReg & ~spi_pkg.XSP_CR_TRANS_INHIBIT_MASK
        AxiQspi.write(spi_pkg.XSP_CR_OFFSET, ControlReg)

        StatusReg = AxiQspi.read(spi_pkg.XSP_SR_OFFSET)
        while (StatusReg & spi_pkg.XSP_SR_TX_EMPTY_MASK) == 0:
            StatusReg = AxiQspi.read(spi_pkg.XSP_SR_OFFSET)
        
        # DEBUG
        # print('XSP_RFO_OFFSET  : 0x{0:08x}'.format(AxiQspi.read(XSP_RFO_OFFSET)))
        ControlReg = AxiQspi.read(spi_pkg.XSP_CR_OFFSET)
        ControlReg = ControlReg | spi_pkg.XSP_CR_TRANS_INHIBIT_MASK
        AxiQspi.write(spi_pkg.XSP_CR_OFFSET, ControlReg)

    AxiQspi.write(spi_pkg.XSP_SSR_OFFSET, spi_pkg.SLAVE_NO_SELECTION)

    # print("ReadResponse")
    resp = []
    RxFifoStatus = AxiQspi.read(spi_pkg.XSP_SR_OFFSET) & 0x01
    while RxFifoStatus == 0:
        temp = AxiQspi.read(spi_pkg.XSP_RFO_OFFSET)
        # DEBUG
        # print('XSP_RFO_OFFSET  : 0x{0:08x}'.format(temp))
        temp = AxiQspi.read(spi_pkg.XSP_DRR_OFFSET)
        # DEBUG
        # print('XSP_DRR_OFFSET  : 0x{0:02x}'.format(temp)) 
        
        resp.append(temp)
        RxFifoStatus = AxiQspi.read(spi_pkg.XSP_SR_OFFSET) & 0x01

    return resp