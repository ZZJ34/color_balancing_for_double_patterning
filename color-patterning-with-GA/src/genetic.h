//Created by KUAN HAO CHEN
//b04b01047
//Genetic algorithm
#ifndef _GENETIC_H_
#define _GENETIC_H_

#include <cstring>
#include <fstream>
#include <iostream>
#include <queue>
#include <string>
#include <sstream>
#include <vector>
#include "shape.h"
using namespace std;



class chromo_typ
{
    private:
    	//the binary bit string is held in a std::string
    	//variable
    	string    bits;
    	double     fitness;

    public:
	 	//Constructor
	    chromo_typ(int num_group,Coloring_Bounding_Box Box);
	    chromo_typ(int num_group,string bts,Coloring_Bounding_Box Box);
	    chromo_typ();
	    
	    



	    //function
	    double Get_fitness();
		string Get_Bits();

		void update(Coloring_Bounding_Box Box);//renew fitness
		string  GetRandomBits(int length);
		int     BinToDec(string bits);
		
		double Calculate_fitness(Coloring_Bounding_Box Box);
		void AssignFitness(Coloring_Bounding_Box Box);
		

		void    PrintChromo();
		vector<int>  output();
 
};


class genome
{
	private:
		vector<chromo_typ> chromosomes;
		

	public:
		genome(vector<chromo_typ> chromosome,Coloring_Bounding_Box Box,int number_group,int pop_size);
		int num_group;
		int POP_SIZE;
		double total_fitness;
		Coloring_Bounding_Box box;

		string  Roulette(int total_fitness, vector<chromo_typ> Population);
		void    Mutate(string &bits);
		void    Crossover(string &offspring1, string &offspring2);
		
		double Calculate_Totalfitness();
		void reproduce();
		void evolve();

		chromo_typ GetBestGene();

};



#endif