#include "shape.h"
#include "genetic.h"
#include <cstring>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <queue>
#include <string>
#include <sstream>
#include <vector>
using namespace std;
#define POP_SIZE 100


int main() {

    srand((int)time(NULL));
    
    char input[] = "my_input.case2";
    
    Coloring_Bounding_Box box = Coloring_Bounding_Box(input);
	
    


    
    int length_gene = box.groups_num;
    

    //initialize chromosomes(the vector of chromo_typ)
    vector<chromo_typ> chromosomes;
    for(int i = 0;i<POP_SIZE;i++){
        chromo_typ chromo(length_gene,box);
        chromosomes.push_back(chromo);
    }
	
    //initialize genome
    genome pop(chromosomes,box,length_gene,POP_SIZE);
    


    chromo_typ best_gene(length_gene,box);//Store the best gene
    
    //Run 10 times in case of being trapped in local maximum
    for(int i = 0; i< 10;i++){
        
        //The process of evolution
        for(int j = 0;j<20;j++){
            pop.evolve();
        }
        
        //Find the best gene
        pop.GetBestGene().PrintChromo();
        if(pop.GetBestGene().Get_fitness()>best_gene.Get_fitness()){
            best_gene = pop.GetBestGene();
        }
    

    }

    cout << "The best gene is ";
    best_gene.PrintChromo();
    cout << "The best score is " << best_gene.Get_fitness()<<endl;
     

	// Calculate the final result     
    box.color_all_groups(best_gene.output());
    box.calDensity();
    cout << "======================================" <<endl;
    cout << "getScore(): " << box.getScore() <<endl;
    box.write_file("my_input.output");


	return 0;
}
