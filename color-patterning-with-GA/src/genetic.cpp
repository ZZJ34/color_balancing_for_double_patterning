//Created by KUAN HAO CHEN
//b04b01047
//Genetic algorithm


#include <algorithm>
//#include <cstring>
#include <string>
#include <fstream>
#include <iostream>
#include <queue>
#include <string>
#include <sstream>
#include <vector>
#include <cstdlib>
#include <cmath>
#include "genetic.h"
#include "shape.h"
using namespace std;



#define CROSSOVER_RATE            0.7
#define MUTATION_RATE             0.001


#define GENE_LENGTH               1
#define MAX_ALLOWABLE_GENERATIONS   400

//returns a float between 0 & 1
#define RANDOM_NUM      ((float)rand()/(RAND_MAX+1.0))
//Constructor
chromo_typ::chromo_typ(int num_group,Coloring_Bounding_Box Box){
	bits = GetRandomBits(num_group);
	fitness = Calculate_fitness(Box);
}


chromo_typ::chromo_typ(int num_group,string bts,Coloring_Bounding_Box Box){
	bits = bts;
	fitness = Calculate_fitness(Box);
}

chromo_typ::chromo_typ(){
	bits = "";
	fitness = 0.0;
}
//		member function

double chromo_typ::Get_fitness(){
	return fitness;
}



string chromo_typ::Get_Bits()
{
	return bits;
}

//
//  This function returns a string of random 1s and 0s of the desired length.
//
//-----------------------------------------------------------------------------------------
string  chromo_typ::GetRandomBits(int length)
{
    string bits;
 
    for (int i=0; i<length; i++)
    {
        if (RANDOM_NUM > 0.5f)
 
            bits += "1";
 
        else
 
            bits += "0";
    }
 
    return bits;
}
 
//---------------------------------BinToDec-----------------------------------------
//
//  converts a binary string into a decimal integer
//
//-----------------------------------------------------------------------------------
int chromo_typ::BinToDec(string bits)
{
    int val          = 0;
    int value_to_add = 1;
 
    for (int i = bits.length(); i > 0; i--)
    {
         
 
        if (bits.at(i-1) == '1')
 
            val += value_to_add;
 
        value_to_add *= 2;
     
    }//next bit
 
    return val;
}
 
 
//---------------------------------Get_fitness------------------------------------------
//According to the area of CA and CB, calculate the fitness
//         It is still unfinished
// 
// 
//------------------------------------------------------------------------------------
double chromo_typ::Calculate_fitness(Coloring_Bounding_Box Box)
{
     Box.color_all_groups(output());

     double score = Box.getScore();

     /*
     for(int i = 0;i<bits.length();i++){
        
        score += stoi(bits.substr(i,1));
     }
    */
    return score;
}




void chromo_typ::AssignFitness(Coloring_Bounding_Box Box)
{
     fitness = Calculate_fitness(Box);
    
}    
void chromo_typ::update(Coloring_Bounding_Box Box){
 	AssignFitness(Box);
 }
//---------------------------------PrintChromo---------------------------------------
//
// decodes and prints a chromo to screen
//-----------------------------------------------------------------------------------
void chromo_typ::PrintChromo()
{   
    //holds decimal values of gene sequence   
         
    int num_elements = bits.length();
     
    for (int i=0; i<num_elements; i++)
    {
        cout<<bits[i];
    }
    cout<<endl;
    
}
vector<int> chromo_typ::output()
{
   vector<int> gene;
   for(int i = 0;i<bits.length();i++){
        
        gene.push_back(stoi(bits.substr(i,1)));
     }
   return gene;
}
//--------------------------------------PrintGeneSymbol-----------------------------
//  
//  given an integer this function outputs its symbol to the screen 
//----------------------------------------------------------------------------------

 

genome::genome(vector<chromo_typ> chromosome,Coloring_Bounding_Box Box,int number_group, int pop_size){
    num_group = number_group;
    POP_SIZE = pop_size;
	chromosomes  = chromosome;
    box = Box;
}
double genome::Calculate_Totalfitness(){
	double TOTAL_FITNESS = 0;
	for(vector<chromo_typ>::iterator chromo = chromosomes.begin(); chromo != chromosomes.end(); ++chromo){
		TOTAL_FITNESS += chromo->Get_fitness();
	}
	return TOTAL_FITNESS;
}


//------------------------------------Mutate---------------------------------------
//
//  Mutates a chromosome's bits dependent on the MUTATION_RATE
//-------------------------------------------------------------------------------------
void genome::Mutate(string &bits)
{
    
    
    for (int i=0; i<bits.length(); i++)
    {
        if (RANDOM_NUM < MUTATION_RATE)
        {
            if (bits.at(i) == '1')
 
                bits.at(i) = '0';
 
            else
 
                bits.at(i) = '1';
        }
    }
    
    return;
}
 
//---------------------------------- Crossover ---------------------------------------
//
//  Dependent on the CROSSOVER_RATE this function selects a random point along the 
//  lenghth of the chromosomes and swaps all the  bits after that point.
//------------------------------------------------------------------------------------
void genome::Crossover(string &offspring1, string &offspring2)
{
  
  //dependent on the crossover rate
  if (RANDOM_NUM < CROSSOVER_RATE)
  {
    
    //create a random crossover point
    int crossover = (int) (RANDOM_NUM * (num_group-1));
    
    string t1 = offspring1.substr(0, crossover) + offspring2.substr(crossover, num_group);
    string t2 = offspring2.substr(0, crossover) + offspring1.substr(crossover, num_group);
    
    offspring1 = t1; offspring2 = t2;                 
  }
  
}
 
 
//--------------------------------Roulette-------------------------------------------
//
//  selects a chromosome from the population via roulette wheel selection
//------------------------------------------------------------------------------------
string genome::Roulette(int total_fitness, vector<chromo_typ> Population)
{
    //generate a random number between 0 & total fitness count
    float Slice = (float)(RANDOM_NUM * total_fitness);
     
    //go through the chromosones adding up the fitness so far
    float FitnessSoFar = 0.0f;
     
    for (int i=0; i<POP_SIZE; i++)
    {
        FitnessSoFar += Population[i].Get_fitness();
         
        //if the fitness so far > random number return the chromo at this point
        if (FitnessSoFar >= Slice)
            
            return Population[i].Get_Bits();
    }
 
    return "";
}






void genome::reproduce(){
	total_fitness = Calculate_Totalfitness();
	vector<chromo_typ> temp;
    int cPop = 0;
    
    //loop until we have created POP_SIZE new chromosomes
    while (cPop < POP_SIZE)
    {
        
        // we are going to create the new population by grabbing members of the old population
        // two at a time via roulette wheel selection.
        string offspring1 = Roulette(total_fitness, chromosomes);
        string offspring2 = Roulette(total_fitness, chromosomes);
        
        //add crossover dependent on the crossover rate
        Crossover(offspring1, offspring2);
        
        //now mutate dependent on the mutation rate
        Mutate(offspring1);
        Mutate(offspring2);
        
        //add these offspring to the new population. (assigning zero as their
        //fitness scores)
        
        temp.push_back(chromo_typ(num_group,offspring1,box));
        cPop++;
        temp.push_back(chromo_typ(num_group,offspring2,box));
        cPop++;
    }//end loop
    
    //copy temp population into main population array
    chromosomes.clear();
    for (int i=0; i<POP_SIZE; i++)
    {
        chromosomes.push_back(temp[i]);
    }

}
void genome::evolve(){
	
    for(vector<chromo_typ>::iterator chromo = chromosomes.begin(); chromo != chromosomes.end(); chromo++){
		chromo->update(box);
	}
    
	reproduce();
    
}
chromo_typ genome::GetBestGene(){
    double BestFitness = 0.0;
    int Best;
    for(int i = 0;i<chromosomes.size();i++){
        if (chromosomes[i].Get_fitness() > BestFitness){
            BestFitness = chromosomes[i].Get_fitness();
            Best = i;
        }
    }
    return chromosomes[Best];

}
