package accumulator_pkg;

    typedef enum logic [1:0] {
        HOLD = 2'b00,
        LOAD = 2'b01,
        ADD  = 2'b10,
        SUB  = 2'b11
    } operation_t;

endpackage
