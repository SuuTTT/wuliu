@startuml

package "Data Processing Module" {
    :Read JSON file;
    :Extract 'spdd' (Order details);
    :Extract 'ck' (Warehouse details);
    :Convert 'spdd' and 'ck' to  (A1, A2, A3);
    :Calculate order priorities (W1);
    :Calculate warehouse priorities (W2);
}

package "Optimization Module" {
    :Pass A1, A2, A3, W1, W2 to logistics_distribution function;
    :logistics_distribution function begins;
    :Establish the optimization problem with constraints;
    :Run the optimization algorithm;
    :Generate distribution plan;
}

package "Output Processing Module" {
    :Transform distribution plan to desired output format;
    :Save/Display the output;
}

@enduml

@startuml
rectangle "Genetic Algorithm (GA)" as GA {
    :Initialize population;
    :Calculate fitness;
    :Selection;
    :Crossover;
    :Mutation;
    :Calculate fitness;
    :Satisfy stop criterion?; 
}
@enduml