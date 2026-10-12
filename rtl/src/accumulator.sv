import accumulator_pkg::*;

module accumulator #(
   parameter unsigned WIDTH = 'd8
)(
    input  logic              clk,
    input  logic              rst,
    input  logic              enable,
    input  logic [1:0]        op,
    input  logic [WIDTH-1:0]  data_in,
    output logic [WIDTH-1:0]  acc
);

   always_ff @(posedge clk) begin
      if(rst) begin
         acc <= 'd0;
      end else begin
         if(enable) begin
            case(operation_t'(op))
               HOLD: acc <= acc;
               LOAD: acc <= data_in;
               ADD:  acc <= acc + data_in;
               SUB:  acc <= acc - data_in;
               default: acc <= 'd0;
            endcase
         end
      end
   end

endmodule
