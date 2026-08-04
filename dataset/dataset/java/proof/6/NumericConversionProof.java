import com.fasterxml.jackson.databind.JsonNode; 


public class NumericConversionProof {


    public static void main(String[] args) {
        runTest(12.75);
        runTest(32767.99);   // near short max
        runTest(-45.9);
        runTest(0.4);
        runTest(2147483647);
        runTest(32768);
    }

    static void runTest(double input) {
        JsonNode currentNode = new JsonNode(input);

        short viaInt = (short) currentNode.asInt();
        short viaDouble = (short) currentNode.asDouble();

        System.out.println("Input value: " + input);
        System.out.println("asInt(): " + currentNode.asInt());
        System.out.println("asDouble(): " + currentNode.asDouble());
        System.out.println("(short) asInt(): " + viaInt);
        System.out.println("(short) asDouble(): " + viaDouble);

        if (viaInt == viaDouble) {
            System.out.println("RESULT: SAME final short value");
        } else {
            System.out.println("RESULT: DIFFERENT values (unexpected)");
        }
        System.out.println();

//        System.out.println("Conversion path:");
//        System.out.println("asInt() -> int -> short");
//        System.out.println("asDouble() -> double -> short");
    }
}

