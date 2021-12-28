#ifndef _SHAPE_H_
#define _SHAPE_H_

#include <cstring>
#include <fstream>
#include <iostream>
#include <queue>
#include <string>
#include <sstream>
#include <vector>
using namespace std;


class Color_Density_Window;

class Coor
{
	public:
		Coor();
		Coor(double X, double Y);
		Coor(const Coor& t);
		~Coor();

		bool is_in_window(Color_Density_Window* window);

		double x;
		double y;
	
};

enum Color 
{
	UNCOLORABLE = -1,
	NOCOLOR = 0,
	CA = 1,
	CB = 2 
};

class Shape
{

	public:
		Shape();
		Shape(int left, int bot, int right, int top);
		Shape(Coor left_bot, Coor right_top);
		~Shape();

		int top();
		int bot();
		int left();
		int right();
		
		Coor center_point();

		//Tseng
		int getArea();
		// 
		bool is_above(Shape* obj);
		bool is_below(Shape* obj);
		bool is_left_to(Shape* obj);
		bool is_right_to(Shape* obj);	
	
		bool is_neighbor(Shape* obj); 		
		void connect(Shape* obj);
		
		void show_shape();

		bool is_in_window(Color_Density_Window* window);
		void set_outer_window(Color_Density_Window* window);



		Coor 					left_bottom;
		Coor 					right_top;
		Color 					color;
		int 					id;
		int 					group_id;
		bool 					is_visited;
		Color_Density_Window*  	outer_window;

		static int x_spacing;
		static int y_spacing;
		static int dens_win_size;

		vector<Shape*> neighbor;
		 
};

//Tseng
class Group
{
public:

	Group();
	~Group();
	//Chen
	bool Color_shapes(Color);// Color all the shapes in group
	/* data */

	int id;
	Color start_color; 
	vector <Shape*> shapes;
	int area_A;
	int area_B;
	bool isColorable;

};

class Color_Density_Window
{
public:

	int length;
	double density_A ;
	double density_B ;
	Coor *left_bottom;
	vector <Shape*> Shapes;

	Color_Density_Window();
	Color_Density_Window(int length,Coor *left_bottom);
	~ Color_Density_Window();
	void calDensity();
};
//

class Coloring_Bounding_Box
{
public:
	//Tseng

	//vector <Color_Density_Window*> windows;
	int Top_boundary;
	int Right_boundary;
	int Left_boundary;
	int Bottom_boundary;
	int density_window_size;// = omega;

	//

	Coloring_Bounding_Box();
	Coloring_Bounding_Box(char file_name[]);
	~Coloring_Bounding_Box();

	void read_file(char file_name[]);
	void input(fstream& fs);
	void write_file(char file_name[]);

	//Tseng
	void build_density_window();
	void calDensity();
	void set_density_windows();
	void setGroups();
	void setBounding();
	double getScore();
	//

	void show_box();

	//Chen
	void mark_color_state();
	//Tseng

	void color_all_groups(vector<int> color_sequence);
	
	vector<Shape*> shapes;
	vector<Color_Density_Window*> windows;
	vector<Group*> Groups;
	int groups_num;
};






#endif