import accumulator_pkg::*;

module accumulator_tb();
   parameter unsigned WIDTH = 'd8;

   logic clk;
   logic rst;
   logic w_enable;
   logic [1:0]       w_op;
   logic [WIDTH-1:0] w_data_in;
   logic [WIDTH-1:0] w_acc;

   accumulator #(
      .WIDTH(WIDTH)
   ) uu_accumulator (
       .clk    (clk      ),
       .rst    (rst      ),
       .enable (w_enable ),
       .op     (w_op     ),
       .data_in(w_data_in),
       .acc    (w_acc    )
   );

   always #5 clk = ~clk;

   initial begin
      $fsdbDumpfile("waves.fsdb");
      $fsdbDumpvars(0, accumulator_tb);
   end

   initial begin
      clk       = 1'b0;
      rst       = 1'b1;
      w_enable  = 1'b0;
      w_op      = HOLD;
      w_data_in = 'd0;

      repeat(2) @(posedge clk);
      rst      = 1'b0;
      w_enable = 1'b1;

      @(posedge clk);
      w_op = LOAD;
      w_data_in = 20;

      // LOAD
      @(posedge clk) begin
         #1
         $display("LOAD 20 --> [ACC = %0d]", w_acc);
      end

      // ADD
      w_op = ADD;
      w_data_in = 5;
      @(posedge clk);
      #1;
      $display("ADD 5 --> [ACC = %0d]", w_acc);

      // SUB
      w_op = SUB;
      w_data_in = 10;
      @(posedge clk);
      #1;
      $display("SUB 10 --> [ACC = %0d]", w_acc);

      // SUB
      w_op = HOLD;
      @(posedge clk);
      #1;
      $display("HOLD --> [ACC = %0d]", w_acc);

      // DISABLE
      w_enable  = 1'b0;
      w_op      = ADD;
      w_data_in = 100;
      @(posedge clk);
      #1;
      $display("DISABLE --> [ACC = %0d]", w_acc);

      // DISABLE
      w_enable  = 1'b1;
      w_op      = LOAD;
      w_data_in = 100;
      @(posedge clk);
      #1;
      $display("LOAD 100 --> [ACC = %0d]", w_acc);

      #20;
      $finish;

   end

endmodule
