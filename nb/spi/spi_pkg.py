XSP_DGIER_OFFSET  = 0x1C
XSP_IISR_OFFSET   = 0x20
XSP_IIER_OFFSET   = 0x28
XSP_SRR_OFFSET    = 0x40  # Software reset register
XSP_CR_OFFSET     = 0x60  # SPI control register
XSP_SR_OFFSET     = 0x64  # SPI status register
XSP_DTR_OFFSET    = 0x68  # SPI data transmit register. A singleregister or a FIFO
XSP_DRR_OFFSET    = 0x6C  # SPI data receive register. A singleregister or a FIFO
XSP_SSR_OFFSET    = 0x70  # SPI Slave select register
XSP_TFO_OFFSET    = 0x74  # Transmit FIFO occupancy register
XSP_RFO_OFFSET    = 0x78  # Receive FIFO occupancy register
XSP_REGISTERS     = [0x40, 0x60, 0x64, 0x68, 0x6c, 0x70, 0x74, 0x78, 0x1c, 0x20, 0x28]

XSP_SRR_RESET_MASK         = 0x0A
XSP_SR_TX_EMPTY_MASK       = 0x00000004
XSP_SR_TX_FULL_MASK        = 0x00000008
XSP_CR_TRANS_INHIBIT_MASK  = 0x00000100
XSP_CR_LOOPBACK_MASK       = 0x00000001
XSP_CR_ENABLE_MASK         = 0x00000002
XSP_CR_MASTER_MODE_MASK    = 0x00000004
XSP_CR_CLK_POLARITY_MASK   = 0x00000008
XSP_CR_CLK_PHASE_MASK      = 0x00000010
XSP_CR_TXFIFO_RESET_MASK   = 0x00000020
XSP_CR_RXFIFO_RESET_MASK   = 0x00000040
XSP_CR_MANUAL_SS_MASK      = 0x00000080

SLAVE_NO_SELECTION = 0xFFFFFFFF