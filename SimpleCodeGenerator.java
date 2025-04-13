import java.util.*;

public class SimpleCodeGenerator {
    static int NUM_REGISTERS;
    static String[] registerDescriptor;
    static Map<String, String> addressDescriptor = new HashMap<>();
    static Queue<Integer> freeRegisters = new LinkedList<>();

    static int getReg(String var) {
        if (addressDescriptor.containsKey(var) && addressDescriptor.get(var).startsWith("R")) {
            return Integer.parseInt(addressDescriptor.get(var).substring(1));
        }

        if (!freeRegisters.isEmpty()) {
            int reg = freeRegisters.poll();
            registerDescriptor[reg] = var;
            addressDescriptor.put(var, "R" + reg);
            return reg;
        }

        int regToSpill = 0; 
        String spilledVar = registerDescriptor[regToSpill];

        System.out.println("STORE " + spilledVar + ", MEM[" + spilledVar + "]");
        addressDescriptor.put(spilledVar, "MEM[" + spilledVar + "]");

        registerDescriptor[regToSpill] = var;
        addressDescriptor.put(var, "R" + regToSpill);
        return regToSpill;
    }

    static void freeReg(String var) {
        if (addressDescriptor.containsKey(var) && addressDescriptor.get(var).startsWith("R")) {
            int reg = Integer.parseInt(addressDescriptor.get(var).substring(1));
            freeRegisters.add(reg);
            registerDescriptor[reg] = null;
            addressDescriptor.remove(var);
        }
    }

    static void printRegisterDescriptor() {
        System.out.println("\nRegister Descriptor:");
        for (int i = 0; i < NUM_REGISTERS; i++) {
            System.out.println("R" + i + " -> " + (registerDescriptor[i] == null ? "empty" : registerDescriptor[i]));
        }
        System.out.println();
    }

    static void generateCode(List<String> TAC) {
        for (String line : TAC) {
            String[] tokens = line.split(" ");
            String result = tokens[0];  
            String op1 = tokens[2];     
            String op = tokens[3];      
            String op2 = tokens[4];     

            int reg1 = getReg(op1);
            System.out.println("MOV " + op1 + ", R" + reg1);

            System.out.println(op.toUpperCase() + " " + op2 + ", R" + reg1);
            
            registerDescriptor[reg1] = result; 
            addressDescriptor.put(result, "R" + reg1);

            System.out.println("Register Descriptor: R" + reg1 + " will hold " + result);
            printRegisterDescriptor();
        }

        System.out.println("MOV " + addressDescriptor.get("X") + ", X");
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        
        System.out.print("Enter number of registers: ");
        NUM_REGISTERS = scanner.nextInt();
        registerDescriptor = new String[NUM_REGISTERS];

        // Initialize free registers queue
        for (int i = 0; i < NUM_REGISTERS; i++) {
            freeRegisters.add(i);
        }

        List<String> TAC = Arrays.asList(
            "T1 = a + b",
            "T2 = c + d",
            "T3 = e - T2",
            "X = T1 - T3"
        );

        System.out.println("\nGenerated Assembly Code:");
        generateCode(TAC);

        scanner.close();
    }
}
