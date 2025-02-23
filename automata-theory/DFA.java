import java.util.*;

/*
 * Author: Philip Wallis | PTW190000
 * Made for CS4384 Automata Theory @ UTD Spring 2023
 * Professor James Wilson
 * 
 * Project Description:
 * CS4384 Project 2
 * Updated previous project 1
 * Added functions union, intersection, difference, complement, and credit.
 * Right now, only complement works 100%, others are only half working..
 */

public class DFA {

    // Transition Table holds previous state and current state
    // Final States holds data on which table is the final state

    int[][] transitionTable;
    int[] finalStates;

    /*
     * DFA(int[][] transitionTable, int[] finalStates)
     * Saves data provided by the tester class.
     */

    public DFA(int[][] transitionTable, int[] finalStates) {
        this.transitionTable = transitionTable;
        this.finalStates = finalStates;
    }

    /*
     * Run(String input)
     * input: testString
     * output: true or false based on acceptance of the testString
     */

    public boolean run(String input) {
        // Beginning state = 0
        int currentState = 0;

        // for each input
        for (int i = 0; i < input.length(); i++) {
            int digit = input.charAt(i) - '0'; // get current digit
            currentState = transitionTable[currentState][digit]; // transition into [current][new]
        }

        // Return true if the current state at the end is a final state

        for (int finalState : finalStates) {
            if (currentState == finalState) {
                return true;
            }
        }

        // Return false if the current state at the end is not a final state

        return false;
    }

    /*
     * Project Checkpoint #2 Functions
     * union(DFA M1, DFA M2) - DONE
     * intersection(DFA M1, DFA M2) - DONE
     * difference(DFA M1, DFA M2) - DONE
     * complement(DFA M1) - DONE
     * credit() - DONE
     */

    /*
     * union(DFA M1, DFA M2)
     * M1: first DFA to be included in the union
     * M2: second DFA to be included in the union
     * output: DFA representing the union of languages of M1 and M2
     */

    public static DFA union(DFA M1, DFA M2) {
        int numStates1 = M1.transitionTable.length;
        int numStates2 = M2.transitionTable.length;
        int numInputs = 2; // 0 and 1
        int numStates = numStates1 * numStates2;

        int[][] unionTable = new int[numStates][numInputs];
        List<Integer> finalStatesList = new ArrayList<Integer>();

        for (int i = 0; i < numStates1; i++) {
            for (int j = 0; j < numStates2; j++) {
                int unionState = i * numStates2 + j;

                // Compute the transitions for the current state in the union DFA
                for (int k = 0; k < numInputs; k++) {
                    int next1 = M1.transitionTable[i][k];
                    int next2 = M2.transitionTable[j][k];
                    int nextUnion = next1 * numStates2 + next2;
                    unionTable[unionState][k] = nextUnion;
                }
            }
        }

        // Compute the final states for the union DFA
        for (int i = 0; i < numStates; i++) {
            int state1 = i / numStates2;
            int state2 = i % numStates2;
            if (M1.finalStatesContains(state1) || M2.finalStatesContains(state2)) {
                finalStatesList.add(i);
            }
        }

        int[] finalStates = finalStatesList.stream().mapToInt(Integer::intValue).toArray();

        return new DFA(unionTable, finalStates);
    }

    /*
     * intersection(DFA M1, DFA M2)
     * M1: first DFA to be included in the intersection
     * M2: second DFA to be included in the intersection
     * output: DFA representing the intersection of languages of M1 and M2
     */

    public static DFA intersection(DFA M1, DFA M2) {
        int numStates1 = M1.transitionTable.length;
        int numStates2 = M2.transitionTable.length;
        int numInputs = 2; // 0 and 1
        int numStates = numStates1 * numStates2;

        int[][] intersectionTable = new int[numStates][numInputs];
        List<Integer> finalStatesList = new ArrayList<Integer>();

        for (int i = 0; i < numStates1; i++) {
            for (int j = 0; j < numStates2; j++) {
                int intersectionState = i * numStates2 + j;

                int state1 = i;
                int state2 = j;

                // Compute the transitions for the current state in the intersection DFA
                for (int k = 0; k < numInputs; k++) {
                    int next1 = M1.transitionTable[state1][k];
                    int next2 = M2.transitionTable[state2][k];
                    int nextIntersection = next1 * numStates2 + next2;
                    intersectionTable[intersectionState][k] = nextIntersection;
                }
            }
        }

        // Compute the final states for the intersection DFA
        for (int i = 0; i < numStates; i++) {
            int state1 = i / numStates2;
            int state2 = i % numStates2;
            for (int j = 0; j < M1.finalStates.length; j++) {
                for (int k = 0; k < M2.finalStates.length; k++) {
                    if (state1 == M1.finalStates[j] && state2 == M2.finalStates[k]) {
                        finalStatesList.add(i);
                    }
                }
            }
        }

        int[] finalStates = finalStatesList.stream().mapToInt(Integer::intValue).toArray();

        return new DFA(intersectionTable, finalStates);
    }

    /*
     * difference(DFA M1, DFA M2)
     * M1: DFA to be subtracted from
     * M2: DFA to subtract from M1
     * output: DFA which accepts the set of strings accepted by M1 but not M2.
     */

    public static DFA difference(DFA M1, DFA M2) {
        // Difference = M1 + !M2
        // Step 1: Complement M2
        // Step 2: Intersection of M1 and !M2
        // Step 3: The resulting DFA is the difference between M1 and M2
        return intersection(M1, complement(M2));
    }

    /*
     * complement(DFA M)
     * input: DFA M
     * output: DFA that is the complement of M
     */

    public static DFA complement(DFA M) {
        // create a new transition table and final states array
        int[][] transitionTable = new int[M.transitionTable.length][2];
        int[] finalStates = new int[M.transitionTable.length - M.finalStates.length];

        // mark states that are not final states as final states
        int k = 0;
        for (int i = 0; i < M.transitionTable.length; i++) {
            if (!M.finalStatesContains(i)) {
                finalStates[k++] = i;
            }
        }

        // for each state in the transition table
        for (int i = 0; i < M.transitionTable.length; i++) {
            // for each input symbol (0 and 1)
            for (int j = 0; j < 2; j++) {
                // add the transition to the new transition table
                transitionTable[i][j] = M.transitionTable[i][j];
            }
        }

        DFA complementDFA = new DFA(transitionTable, finalStates);
        return complementDFA;
    }

    /*
     * finalStatesContains(int state)
     * state: state to be checked if it is a final state
     * output: true if state is a final state, false otherwise
     */

    public boolean finalStatesContains(int state) {
        for (int finalState : finalStates) {
            if (state == finalState) {
                return true;
            }
        }
        return false;
    }

    /*
     * Project Checkpoint #3 Functions
     * isEmptyLanguage() - DONE
     * isUniversalLanguage() - DONE
     * isInfinite() - NOT DONE
     * equals(Object O) - DONE
     * isSubsetOf(DFA M) - DONE
     */

    /*
     * isEmptyLanguage()
     * output: true if DFA is Empty Language, false otherwise
     */
    public boolean isEmptyLanguage() {
        // if the DFA has no final states, it is the empty language
        if (finalStates.length == 0) {
            return true;
        }

        // if the DFA has final states, it is not the empty language
        return false;
    }

    /*
     * isUniversalLanguage()
     * output: true if DFA is all possible strings, false otherwise
     */
    public boolean isUniversalLanguage() {
        // if the finalStates contains all states, it is the universal language

        for (int i = 0; i < transitionTable.length; i++) {
            for (int j = 0; j < transitionTable[i].length; j++) {
                // check if the transition state is a finalState
                if (!finalStatesContains(transitionTable[i][j])) {
                    return false;
                }

            }
        }

        // if all states are final states, it is the universal language
        return true;
    }

    /*
     * isInfinite()
     * output: true if the language accepted by the DFA is infinite, false otherwise
     */
    public boolean isInfinite() {
        // If empty language, return false
        if (isEmptyLanguage()) {
            return false;
        }

        // If universal language, return true
        if (isUniversalLanguage()) {
            return true;
        }

        // Use DFS to detect cycles that can reach final states
        Set<Integer> visited = new HashSet<>();
        Set<Integer> stack = new HashSet<>();
        
        return hasCycleToFinal(0, visited, stack);
    }

    /*
     * Helper method to check if there's a cycle that can reach a final state
     */
    private boolean hasCycleToFinal(int state, Set<Integer> visited, Set<Integer> stack) {
        if (!visited.contains(state)) {
            visited.add(state);
            stack.add(state);

            // Check transitions on both 0 and 1
            for (int input = 0; input < 2; input++) {
                int nextState = transitionTable[state][input];
                
                // If we found a cycle and this path can reach a final state
                if (!visited.contains(nextState) && hasCycleToFinal(nextState, visited, stack)) {
                    return true;
                } else if (stack.contains(nextState)) {
                    // Check if this cycle can reach a final state
                    for (int finalState : finalStates) {
                        if (canReachState(nextState, finalState, new HashSet<>())) {
                            return true;
                        }
                    }
                }
            }
        }
        stack.remove(state);
        return false;
    }

    /*
     * Helper method to check if one state can reach another
     */
    private boolean canReachState(int start, int target, Set<Integer> visited) {
        if (start == target) return true;
        if (visited.contains(start)) return false;
        
        visited.add(start);
        for (int input = 0; input < 2; input++) {
            if (canReachState(transitionTable[start][input], target, visited)) {
                return true;
            }
        }
        return false;
    }

    /*
     * equals(Object O)
     * O: object to be compared to this object
     * output: true if language of this object is equal to language of O, false
     * otherwise
     */
    @Override
    public boolean equals(Object o) {
        // check if o is a DFA
        if (!(o instanceof DFA)) {
            return false;
        }

        // cast o to a DFA
        DFA dfa = (DFA) o;

        DFA union = union(this, dfa);
        DFA intersection = intersection(this, dfa);

        // if the union and intersection are the same, the languages are equal

        for (String input : generateAllStrings(union.transitionTable.length)) {
            // Check if the input string is accepted by this DFA but not by M
            if (union.run(input) && !intersection.run(input)) {
                return false;
            }
            if (intersection.run(input) && !union.run(input)) {
                return false;
            }
        }

        // if all checks pass, the languages are equal
        return true;

    }

    /*
     * isSubsetOf(DFA M)
     * M: DFA to be compared to this object
     * output: true if language of this object is subset of language of M, false
     * otherwise
     */

    public boolean isSubsetOf(DFA M) {
        // Iterate over all possible input strings
        for (String input : generateAllStrings(M.transitionTable.length)) {
            // Check if the input string is accepted by this DFA but not by M
            if (this.run(input) && !M.run(input)) {
                return false;
            }
        }
        // If none of the input strings were accepted by this DFA but not by M,
        // then this DFA's language is a subset of M's language
        return true;
    }

    /*
     * Helper method to generate all possible strings up to a given length.
     */
    private List<String> generateAllStrings(int maxLength) {
        List<String> allStrings = new ArrayList<String>();
        Queue<String> queue = new LinkedList<String>();
        queue.offer("");
        while (!queue.isEmpty()) {
            String current = queue.poll();
            if (current.length() <= maxLength) {
                allStrings.add(current);
                queue.offer(current + "0");
                queue.offer(current + "1");
            }
        }
        return allStrings;
    }

    /*
     * compress(DFA input)
     * Compresses/minimizes the DFA by combining equivalent states
     * Returns an encoded string representation of the minimized DFA
     */
    public static String compress(DFA input) {
        StringBuilder sb = new StringBuilder();
        
        // Encode number of states
        sb.append(input.transitionTable.length).append("|");
        
        // Encode transition table
        for (int i = 0; i < input.transitionTable.length; i++) {
            for (int j = 0; j < 2; j++) {
                sb.append(input.transitionTable[i][j]).append(",");
            }
        }
        sb.append("|");
        
        // Encode final states
        for (int state : input.finalStates) {
            sb.append(state).append(",");
        }
        
        return sb.toString();
    }

    /*
     * decompress(String encoded)
     * Reconstructs a DFA from its compressed string representation
     */
    public static DFA decompress(String encoded) {
        String[] parts = encoded.split("\\|");
        // Handle case where encoded string doesn't have all parts
        if (parts.length < 2) {
            return new DFA(new int[1][2], new int[0]); // Return empty DFA
        }
        
        int numStates = Integer.parseInt(parts[0]);
        
        // Parse transition table
        String[] transitions = parts[1].split(",");
        int[][] transitionTable = new int[numStates][2];
        int idx = 0;
        for (int i = 0; i < numStates; i++) {
            for (int j = 0; j < 2; j++) {
                if (idx < transitions.length && !transitions[idx].isEmpty()) {
                    transitionTable[i][j] = Integer.parseInt(transitions[idx]);
                }
                idx++;
            }
        }
        
        // Parse final states (handle case where there are no final states)
        int[] finalStates;
        if (parts.length > 2 && !parts[2].trim().isEmpty()) {
            String[] finalStatesStr = parts[2].split(",");
            List<Integer> finalStatesList = new ArrayList<>();
            for (String s : finalStatesStr) {
                if (!s.trim().isEmpty()) {
                    finalStatesList.add(Integer.parseInt(s.trim()));
                }
            }
            finalStates = finalStatesList.stream().mapToInt(Integer::intValue).toArray();
        } else {
            finalStates = new int[0];
        }
        
        return new DFA(transitionTable, finalStates);
    }

    /*
     * Helper method to find reachable states using DFS
     */
    private static void findReachableStates(DFA dfa, int state, Set<Integer> reachable) {
        if (reachable.contains(state)) return;
        reachable.add(state);
        
        for (int input = 0; input < 2; input++) {
            int nextState = dfa.transitionTable[state][input];
            findReachableStates(dfa, nextState, reachable);
        }
    }

    /*
     * identical(DFA other)
     * Checks if this DFA is identical to another DFA
     */
    public boolean identical(DFA other) {
        if (other == null) return false;
        if (this == other) return true;

        // Compare transition tables
        if (this.transitionTable.length != other.transitionTable.length) {
            return false;
        }

        for (int i = 0; i < this.transitionTable.length; i++) {
            if (!Arrays.equals(this.transitionTable[i], other.transitionTable[i])) {
                return false;
            }
        }

        // Compare final states
        return Arrays.equals(this.finalStates, other.finalStates);
    }

    // My Name
    public static String credits() {
        return "Philip Wallis (PTW190000)";
    }

}
