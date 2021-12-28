#include <algorithm>
#include <cstring>
#include <fstream>
#include <iostream>
#include <iomanip>
#include <queue>
#include <string>
#include <sstream>
#include <vector>
#include <cmath>
#include "shape.h"
using namespace std;

#define NO_ID -1

//************************************************************************************
//************************************************************************************
//************************************************************************************

// Class: Coor

//************************************************************************************
//************************************************************************************
//************************************************************************************


Coor::Coor () {}
Coor::Coor(double X, double Y):x(X), y(Y) {}
Coor::Coor(const Coor& t):x(t.x), y(t.y){}
Coor::~Coor() {}

bool Coor::is_in_window(Color_Density_Window* window)
{
	int win_left = window->left_bottom->x;
	int win_bot = window->left_bottom->y;
	int win_length = window->length;

	if(this->x > win_left && this->y > win_bot)
		if(this->x <= (win_left + win_length) && this->y <= (win_bot + win_length))
			return true;

	return false;
}


//************************************************************************************
//************************************************************************************
//************************************************************************************

// Class: Shape

//************************************************************************************
//************************************************************************************
//************************************************************************************


Shape::Shape() 
{}

Shape::Shape(int left, int bot, int right, int top):left_bottom(left, bot), right_top(right, top), is_visited(false), group_id(NO_ID), color(NOCOLOR)
{}

Shape::Shape(Coor left_bottom, Coor right_top):left_bottom(left_bottom), right_top(right_top), is_visited(false), group_id(NO_ID), color(NOCOLOR) {}

Shape::~Shape() {}

int Shape::top()	{ return right_top.y; }
int Shape::bot()	{ return left_bottom.y;  }
int Shape::left()	{ return left_bottom.x;  }
int Shape::right()	{ return right_top.x; }

Coor Shape::center_point()
{
	double center_x = (left_bottom.x + right_top.x)/2;
	double center_y = (left_bottom.y + right_top.y)/2;
	Coor output = Coor(center_x, center_y);
	return output;
}

//Tseng
int Shape::getArea() {return (top()-bot())*(right()-left());}

		 
bool Shape::is_above(Shape* obj) 	{ return obj->top()   < this->bot()?    true : false;   }
bool Shape::is_below(Shape* obj) 	{ return obj->bot()   > this->top()?    true : false;   }
bool Shape::is_left_to(Shape* obj)	{ return obj->left()  > this->right()?  true : false;   }
bool Shape::is_right_to(Shape* obj) { return obj->right() < this->left()?   true : false;   }	
	
bool Shape::is_neighbor(Shape* obj)
{
	int delta = 0;
	if (!is_above(obj) && !is_below(obj))
	{
		if(this->is_right_to(obj))
			delta = this->left() - obj->right();
		else if (this->is_left_to(obj))
			delta = obj->left() - this->right();
		else
			return false;

		if (delta <= x_spacing)
			return true;
		else
			return false;				
	}
	else if (!is_right_to(obj) && !is_left_to(obj))
	{
		if (this->is_above(obj))
			delta = this->bot() - obj->top();
		else if (this->is_below(obj))
			delta = obj->bot() - this->top();
		else 
			return false;
			
		if (delta <= y_spacing)
			return true;
		else
			return false;
	}
	else
		return false;
} 		

void Shape::connect(Shape* obj)
{
	neighbor.push_back(obj);
}
	
void Shape::show_shape()
{
	cout << left() << "," << bot() << "," << right() << "," << top() << "\t";
	cout << "(" << (color==UNCOLORABLE? "UNCOLORABLE": (color==CA? "CA":(color==CB? "CB":"NOCOLOR"))) << ")" << "\t";
	cout << "group_id: " << group_id << endl;
}

bool Shape::is_in_window(Color_Density_Window* window)
{
	if(this->center_point().is_in_window(window))
		return true;
	else		
		return false;
}

void Shape::set_outer_window(Color_Density_Window *window)
{
	if (is_in_window(window))
	{
		outer_window = window;
	}
}



// Chen. 06/09
int Shape::x_spacing;
int Shape::y_spacing;
int Shape::dens_win_size;

//************************************************************************************
//************************************************************************************
//************************************************************************************

// Class: Coloring_Bounding_Box

//************************************************************************************
//************************************************************************************
//************************************************************************************

Coloring_Bounding_Box::Coloring_Bounding_Box() {}

Coloring_Bounding_Box::Coloring_Bounding_Box(char file_name[])
{
	read_file(file_name);;
	setGroups();
	mark_color_state();

	//	cout << ">>>>>>> Construction <<<<<<<<<" << endl;
	//	show_box();

	setBounding();
	build_density_window();
	set_density_windows();
	calDensity();
	
}

Coloring_Bounding_Box::~Coloring_Bounding_Box() {}

void Coloring_Bounding_Box::read_file(char file_name[])
{
	fstream fs;
	fs.open(file_name, ios::in);
	input(fs);
	fs.close();
}

void Coloring_Bounding_Box::input(fstream& fs)
{
	string temp_string; 
	int alpha;
	int beta; 
	int omega;

	fs >> temp_string;
	
	for (int i = temp_string.size()-1, t = 1; i > 5; --i, t*=10)
	{
		alpha = t * (temp_string[i]-48);
	}

	fs >> temp_string;
	for (int i = temp_string.size()-1, t = 1; i > 4; --i, t*=10)
	{
		beta = t * (temp_string[i]-48);
	}

	fs >> temp_string;
	for (int i = temp_string.size()-1, t = 1; i > 5; --i, t*=10)
	{
		omega = t * (temp_string[i]-48);
	}

	Shape::x_spacing = alpha;
	Shape::y_spacing = beta;
	Shape::dens_win_size = omega;


	while (fs >> temp_string)
	{
		stringstream ss(temp_string);
		Coor temp_coor[2];
		int sub;
		char c;
		int temp[4];

		int i = 0;
		while(ss >> sub)
		{
			temp[i] = sub;
			ss >> c;
			i++;
		}

		temp_coor[0].x = temp[0];
		temp_coor[0].y = temp[1];
		temp_coor[1].x = temp[2];
		temp_coor[1].y = temp[3];

		ss.str("");
		ss.clear();

		Shape* temp_shape = new Shape(temp_coor[0], temp_coor[1]);
		temp_shape -> color = NOCOLOR;
		shapes.push_back(temp_shape);
				
	}

}

void Coloring_Bounding_Box::write_file(char file_name[])
{
	fstream fout(file_name);
	fout.open(file_name, ios::out);
	for (int i = 0; i < windows.size(); ++i)
	{
		int win_left = windows[i]->left_bottom->x;
		int win_right = win_left + windows[i]->length;
		int win_bot = windows[i]->left_bottom->y;
		int win_top = win_bot + windows[i]->length;

		fout << "WIN[" << i+1 << "]=";
		fout << win_left << ",";
		fout << win_bot << ",";
		fout << win_right << ",";
		fout << win_top;
		fout <<  "(" << windows[i]->density_A << " " << windows[i]->density_B << ")" << endl;
	}

	for (int i = 0; i < Groups.size(); ++i)
	{
		fout << "GROUP" << endl;
		if(Groups[i]->isColorable)
		{
			vector<Shape*> CA_shapes;
			vector<Shape*> CB_shapes;

			for (int j = 0; j < Groups[i]->shapes.size(); ++j)
			{
				Shape* current_shape = Groups[i]->shapes[j];

				if (current_shape->color == CA)
				{
					CA_shapes.push_back(current_shape);
				}
				else if (current_shape->color == CB)
				{
					CB_shapes.push_back(current_shape);
				}
			}

			for (int j = 0; j < CA_shapes.size(); ++j)
			{
				fout << "CA[" << j+1 << "]=";
				fout << CA_shapes[j]->left() << ",";
				fout << CA_shapes[j]->bot()<< ",";
				fout << CA_shapes[j]->right() << ",";
				fout << CA_shapes[j]->top() << endl;
			}

			for (int j = 0; j < CB_shapes.size(); ++j)
			{
				fout << "CB[" << j+1 << "]=";
				fout << CB_shapes[j]->left() << ",";
				fout << CB_shapes[j]->bot()<< ",";
				fout << CB_shapes[j]->right()<< ",";
				fout << CB_shapes[j]->top()<< endl;
			}
		}
		else
		{
			for (int j = 0; j < Groups[i]->shapes.size(); ++j)
			{
				fout << "NO[" << j+1 << "]=";
				fout << shapes[j]->left() << ",";
				fout << shapes[j]->bot() << "," ;
				fout << shapes[j]->right() << ",";
				fout << shapes[j]->top() <<  endl;	
			}
		}
	}
}

void Coloring_Bounding_Box::show_box()
{
	cout << "ALPHA=" << Shape::x_spacing << endl;
	cout << "BETA=" << Shape::y_spacing << endl;
	cout << "OMEGA=" << Shape::dens_win_size << endl;
	cout << "\n";
	for (int i = 0; i < Groups.size(); ++i)
	{
		Group* current_group = Groups[i];
		cout << "GROUP" << current_group->id << "\t";
		cout << "isColorable: " << (current_group->isColorable? "true": "false") << "\t";
		cout << "group_size: " << current_group->shapes.size() << endl;

		for (int j = 0; j < current_group->shapes.size(); ++j)
		{
			Shape* current_shape = current_group->shapes[j];
			current_shape->show_shape();
			for (int k = 0; k < current_shape->neighbor.size(); ++k)
			{
					cout << "***";
					current_shape->neighbor[k]->show_shape();
			}
			cout << endl;
		}

		cout << "---------------------------------------" << endl;
	}

}




//Chen
void Coloring_Bounding_Box::mark_color_state(){
	queue<Shape*> visiting_queue;
	queue<Shape*> from_queue;
	bool isColorable = true;

	for (int i = 0; i < Groups.size(); ++i)
	{
		Group* current_group = Groups[i];
		vector<Shape*>::iterator start_shape = Groups[i]->shapes.begin();
		(*start_shape)->is_visited = true;

		visiting_queue.push(*start_shape);				
		
		Shape* s = visiting_queue.front();
		visiting_queue.pop();
		s->is_visited = true;
		
		for (int j = 0; j < s->neighbor.size(); ++j)
		{
			Shape* current_neighbor = s->neighbor[j];
			current_neighbor->is_visited = true;
			visiting_queue.push(current_neighbor);
			from_queue.push(s);
		}
		
		while(!visiting_queue.empty())
		{
			s = visiting_queue.front();
			visiting_queue.pop();
			s->is_visited = true;
						
			Shape* from = from_queue.front();
			from_queue.pop();				

			for (int j = 0; j < s->neighbor.size(); ++j)
			{	

				Shape* current_neighbor = s->neighbor[j];

				if (current_neighbor == from)
				{
					continue;
				}

				if (current_neighbor->is_visited == false)
				{
					current_neighbor->is_visited = true;
					visiting_queue.push(current_neighbor);
					from_queue.push(s);
				}

				if (current_neighbor->is_neighbor(from))
				{					
					isColorable = false;

					std::queue<Shape*> empty;
   					std::swap(visiting_queue, empty);

   					std::queue<Shape*> empty2;
   					std::swap(from_queue , empty2);
   					break;
				}	
								
			}
		}	
		
		if (isColorable){
			isColorable = true;
			current_group->isColorable = true;
			vector<Shape*>::iterator s = current_group->shapes.begin();		
			while(s != current_group->shapes.end()){
				(*s)->color = NOCOLOR;
				(*s)->is_visited = false;
				s++;
			}
		}
		else{
			isColorable = true;
			current_group->isColorable = false;
			vector<Shape*>::iterator s = current_group->shapes.begin();		
			while(s != current_group->shapes.end()){
				(*s)->color = UNCOLORABLE;
				(*s)->is_visited = false;
				s++;
			}
		}
			
	}
}

void Coloring_Bounding_Box::setBounding(){
	int min_left = 999999;
	int Max_right = -999999;
	int Max_top = -999999;
	int min_bottom = 999999;

	density_window_size = shapes[0]->dens_win_size;
	for (int i = 0; i < shapes.size(); ++i)
	{
		if (shapes[i] -> color != -1 )
		{
			if (shapes[i] ->left_bottom.x < min_left)
			{
				min_left = shapes[i] ->left_bottom.x;
			}
			if (shapes[i] ->left_bottom.y < min_bottom)
			{
				min_bottom = shapes[i] ->left_bottom.y;
			}
			if (shapes[i] ->right_top.x > Max_right)
			{
				Max_right = shapes[i] ->right_top.x;
			}
			if (shapes[i] ->right_top.y > Max_top)
			{
				Max_top = shapes[i] ->right_top.y;
			}
		}
	}
	Top_boundary = Max_top;
	Right_boundary = Max_right;
	Left_boundary = min_left;
	Bottom_boundary = min_bottom;
}

void Coloring_Bounding_Box::setGroups(){
	int group_id_counter = 1;
	queue<Shape*> visiting_queue;
	queue<Shape*> from_queue;

	for (int i = 0; i < shapes.size(); ++i)
	{
		
		if(shapes[i]->group_id != NO_ID)
		{
			continue;
		}
		else
		{
			Group *x = new Group();
			x -> id = group_id_counter;
			Groups.push_back(x);

			shapes[i]->group_id = group_id_counter;
			visiting_queue.push(shapes[i]);
			from_queue.push(NULL);
			Groups[group_id_counter-1]->shapes.push_back(shapes[i]);	

			while(!visiting_queue.empty())
			{
				Shape* current_shape = visiting_queue.front();
				Shape* from = from_queue.front();
				visiting_queue.pop();
				from_queue.pop();

				for (int j = 0; j < shapes.size(); ++j)
				{
					if(current_shape->is_neighbor(shapes[j]))
					{
						if (shapes[j] == from)
						{
							current_shape->connect(shapes[j]);
							continue;
						}
						else
						{
							current_shape->connect(shapes[j]);						
								
							if (shapes[j]->group_id == NO_ID)
							{
								Groups[group_id_counter-1]->shapes.push_back(shapes[j]);
								shapes[j]->group_id = group_id_counter;	
								visiting_queue.push(shapes[j]);
								from_queue.push(current_shape);
							}
						}						



					}
				}
			}

			group_id_counter++;
		}
	}

	groups_num = group_id_counter;
}


void Coloring_Bounding_Box::calDensity(){
	for (int i = 0; i < windows.size(); ++i)
	{
		windows[i] -> density_A = 0;
		windows[i] -> density_B = 0;
		windows[i] -> calDensity();
	}
}

void Coloring_Bounding_Box::set_density_windows(){

	for (int i = 0; i < shapes.size(); ++i)
	{
		for (int j = 0; j < windows.size(); ++j)
		{
			if (shapes[i]->color != -1)
			{
				shapes[i]->set_outer_window(windows[j]);
			}
		}
		if(shapes[i]->color != -1){
			shapes[i] -> outer_window -> Shapes.push_back(shapes[i]);
		}
	}
}

double Coloring_Bounding_Box::getScore(){
	double score = 0;
	int size = windows.size();
	calDensity();
	for (int i = 0; i < size; ++i)
	{
		//cout << "density:" << fixed << setprecision(5) << windows[i]->density_A << " " << windows[i]->density_B << endl;
		score = score + (70/size - abs(windows[i] -> density_A - windows[i] -> density_B));	
	}
	//cout << score << endl;
	return score;
}

void Coloring_Bounding_Box::build_density_window(){
	int width = Right_boundary - Left_boundary;
	int height = Top_boundary - Bottom_boundary;
	double x = (double)width/density_window_size;
	double y = (double)height/density_window_size;

	int num_column = ceil(x);
	int num_row = ceil(y);

	for (int i = 1; i <= num_row ; ++i)
	{
		if (i<num_row)
		{
			for (int j = 1; j < num_column ; ++j)
			{
				Coor *left_bottom = new Coor(Left_boundary + (j-1)*density_window_size,Bottom_boundary + (i-1)*density_window_size);
				Color_Density_Window *x = new Color_Density_Window(density_window_size,left_bottom);
				windows.push_back(x);
			}
			Coor *left_bottom = new Coor(Right_boundary - density_window_size,Bottom_boundary + (i-1)*density_window_size);
			Color_Density_Window *x = new Color_Density_Window(density_window_size,left_bottom);
			windows.push_back(x);
		}else{
			for (int j = 1; j < num_column ; ++j)
			{
				Coor *left_bottom = new Coor(Left_boundary + (j-1)*density_window_size,Top_boundary - density_window_size);
				Color_Density_Window *x = new Color_Density_Window(density_window_size,left_bottom);
				windows.push_back(x);
			}
			Coor *left_bottom = new Coor(Right_boundary - density_window_size,Top_boundary - density_window_size);
			Color_Density_Window *x = new Color_Density_Window(density_window_size,left_bottom);
			windows.push_back(x);

		}
	}
}

void Coloring_Bounding_Box::color_all_groups(vector<int> color_sequence){
	mark_color_state();
	for (int i = 0; i < Groups.size(); ++i)
	{
		Group* current_group = Groups[i];
		if (color_sequence[i] == 0){
			current_group->Color_shapes(CA);
		}else{
			current_group->Color_shapes(CB);
		}
		
	}
}



//************************************************************************************
//************************************************************************************
//************************************************************************************

// Class: Color_Density_Window

//************************************************************************************
//************************************************************************************
//************************************************************************************

Color_Density_Window::Color_Density_Window(int length,Coor *left_bottom)
{
	this -> length = length;
	this -> left_bottom = left_bottom;
}


void Color_Density_Window::calDensity(){
	double area_A = 0;//color = 0
	double area_B = 0;//color = 1

	for (int i = 0; i < Shapes.size(); ++i)		
	{
		if (Shapes[i]->color == CA)
		{
			area_A += Shapes[i]->getArea();
		}else if(Shapes[i]->color == CB){
			area_B += Shapes[i]->getArea();
		}
	}
	density_A = (double)area_A / (length*length);
	density_B = (double)area_B / (length*length);
}




//************************************************************************************
//************************************************************************************
//************************************************************************************

// Class: Group

//************************************************************************************
//************************************************************************************
//************************************************************************************

//Chen 06/09
Group::Group(){
}

bool Group::Color_shapes(Color initial){
	
	//initail can be CA or CB
	
	if (!isColorable)
	{
		return false;
	}
	else
	{
		shapes[0]->color = initial;
		for (int i = 0; i < shapes.size(); i++)
		{
			Shape* current_shape = shapes[i];
			vector<Shape*>& current_neighbor = current_shape->neighbor;
			vector<Shape*>::iterator neighbor_it;

			if(current_neighbor.size()>0)
			{
				for(neighbor_it = current_neighbor.begin(); neighbor_it != current_neighbor.end(); ++neighbor_it) 
				{
    				if ((*neighbor_it)->color == NOCOLOR)
    				{
						if(shapes[i]->color == CA)
						{
							(*neighbor_it)->color = CB;
						}
						else if(shapes[i]->color == CB)
						{
							(*neighbor_it)->color = CA;
						}
					}
	 			}
			}
		
		}
	}
	
	for (int i = 0; i < shapes.size(); i++){
		if (shapes[i]->color == NOCOLOR){
			cout << "shape " << i << endl;
			cout << "It is not finished coloring"<<endl;
			break;
		}	
	}
	//cout << "Shapes are all colored"<<endl;
	
	bool is_success = true;
	for (int i = 0; i < shapes.size(); i++){
		for(vector<Shape*>::iterator neighbour = shapes[i]->neighbor.begin(); neighbour != shapes[i]->neighbor.end(); ++neighbour){
			if ((*neighbour)->color == shapes[i]->color){
				cout << "Coloring is invalid"<<endl;
				is_success = false;
				break;
			}
		}
		
	}
	return true;//return it is colorable
}
