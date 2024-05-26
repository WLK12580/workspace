// #include<vtkSmartPointer.h>
 
// #include<vtkConeSource.h>
// #include<vtkPolyDataMapper.h>
// #include<vtkActor.h>
// #include <vtkAxesActor.h>
// #include <vtkLineSource.h>
// #include<vtkRenderer.h>
// #include<vtkRenderWindow.h>
// #include<vtkRenderWindowInteractor.h>
// #include<vtkInteractorStyleTrackballCamera.h>
// // #include "vtkAutoInit.h" 
// // VTK_MODULE_INIT(vtkRenderingOpenGL);
// // VTK_MODULE_INIT(vtkInteractionStyle);
// // VTK_MODULE_INIT(vtkRenderingFreeType)
// #include "vtkAutoInit.h"
// VTK_MODULE_INIT(vtkRenderingOpenGL2);
// VTK_MODULE_INIT(vtkInteractionStyle);
// VTK_MODULE_INIT(vtkRenderingFreeType)
 
// int main()
// {
// 	//圆锥模型
// 	vtkSmartPointer<vtkConeSource> cone = vtkSmartPointer<vtkConeSource>::New();
// 	cone->SetHeight(3.0);
// 	cone->SetRadius(1.0);
// 	cone->SetResolution(10);

// 	vtkSmartPointer<vtkLineSource> lineSource = vtkSmartPointer<vtkLineSource>::New();
// 	double origin[3] = {0.0, 0.0, 0.0};
//     double p0[3] = {0.0, 0.0, 0.0};
//     double p1[3] = {10.0, 10.0, 10.0};
 

// 	vtkSmartPointer<vtkPoints> points = vtkSmartPointer<vtkPoints>::New();
//     points->InsertNextPoint(origin);
//     points->InsertNextPoint(p0);
//     points->InsertNextPoint(p1);
//     lineSource->SetPoints(points);
//     lineSource->Update();


// 	vtkSmartPointer<vtkAxesActor> act=vtkSmartPointer<vtkAxesActor>::New();
// 	act->SetPosition(0, 0, 0);
// 	act->SetTotalLength(10,10,10);
// 	act->SetShaftType(0);
// 	act->SetAxisLabels(0);
// 	act->SetCylinderRadius(0.02);

 
// 	//映射器
// 	vtkSmartPointer<vtkPolyDataMapper> coneMapper = vtkSmartPointer<vtkPolyDataMapper>::New();
// 	coneMapper->SetInputConnection(cone->GetOutputPort());
// 	coneMapper->SetInputConnection(lineSource->GetOutputPort());

	
 
// 	//对象
// 	vtkSmartPointer<vtkActor> coneActor = vtkSmartPointer<vtkActor>::New();
// 	coneActor->SetMapper(coneMapper);
// 	vtkSmartPointer<vtkActor> LineActor = vtkSmartPointer<vtkActor>::New();

 
// 	//渲染
// 	vtkSmartPointer<vtkRenderer>renderer = vtkSmartPointer<vtkRenderer>::New();
// 	renderer->AddActor(coneActor);
// 	renderer->AddActor(act);
// 	renderer->SetBackground(0.0, 1.0, 1.0);
 
// 	//渲染窗口
// 	vtkSmartPointer<vtkRenderWindow>renWin = vtkSmartPointer<vtkRenderWindow>::New();
// 	renWin->AddRenderer(renderer);
// 	renWin->SetSize(600, 400);
 
// 	//交互
// 	vtkSmartPointer<vtkRenderWindowInteractor>renderInteractor = vtkSmartPointer<vtkRenderWindowInteractor>::New();
// 	renderInteractor->SetRenderWindow(renWin);
 
// 	//交互风格
// 	vtkSmartPointer<vtkInteractorStyleTrackballCamera>style = vtkSmartPointer<vtkInteractorStyleTrackballCamera>::New();
// 	renderInteractor->SetInteractorStyle(style);
 
// 	renderInteractor->Initialize();
// 	renderInteractor->Start();
 
// 	return EXIT_SUCCESS;

 
// }

#include <iostream>
using namespace std;
//解决"Error: no override found for vtkRenderWindow"问题
#include <vtkAutoInit.h>
VTK_MODULE_INIT(vtkRenderingOpenGL2); //有时候是：VTK_MODULE_INIT(vtkRenderingOpenGL);都试一下
VTK_MODULE_INIT(vtkInteractionStyle);
VTK_MODULE_INIT(vtkRenderingFreeType);
//引入VTK对象头文件
#include <vtkActor.h>
#include <vtkCellArray.h>
#include <vtkCellData.h>
#include <vtkDoubleArray.h>
#include <vtkNamedColors.h>
#include <vtkPoints.h>
#include <vtkPolyData.h>
#include <vtkPolyDataMapper.h>
#include <vtkPolyLine.h>
#include <vtkProperty.h>
#include <vtkRenderWindow.h>
#include <vtkRenderWindowInteractor.h>
#include <vtkRenderer.h>
#include <vtkSmartPointer.h>
int main(int, char*[])
{
	//圆心位置（根据需要自行更改）
	double circleCenter[3] = {10, 10, 0}; //单位：米。这里给出单位主要是让人有个直观感受，可以根据需要自行更改
	//圆半径（根据需要自行更改）
	double r = 50; //单位：米
	//圆周上的相邻点构成的弦长（相当于圆周分辨率）
	double l = 0.001; //单位：米（根据需要自行更改）
	//核心理论：由弦长和半径计算弧度（画个图就能推导出来）
	double theta = 2 * asin(l / (2 * r));
	//圆周上点的数目
	long long pntNum = (long long)(2 * M_PI / theta);
	//产生圆周上的点（z=0）
	vtkSmartPointer<vtkPoints> points = vtkSmartPointer<vtkPoints>::New();
	for (long long i=0; i<pntNum; i++)
	{
		points->InsertPoint(i, circleCenter[0] + r*cos(i*theta), circleCenter[1] + r*sin(i*theta), 0);
	}
	//注意：vtkPolyLine并没有提供封闭首尾端点的函数，但我们可以在末尾再增加一个点，使其坐标和首点一样即可实现首尾封闭的效果
	//在末尾继续添加一个点，使其与首点相等，从而使图形闭合
	points->InsertPoint(pntNum, circleCenter[0] + r*cos(0*theta), circleCenter[1] + r*sin(0*theta), 0);
	//定义颜色对象，主要用于展示，不定义也无所谓，默认为白色
	vtkSmartPointer<vtkNamedColors> colors = vtkSmartPointer<vtkNamedColors>::New();
	//定义多段线对象并进行设置
	vtkSmartPointer<vtkPolyLine> polyLine = vtkSmartPointer<vtkPolyLine>::New();
	polyLine->GetPointIds()->SetNumberOfIds(pntNum+1);
	for (long long i = 0; i < pntNum + 1; i++)
	{
		//在位置i处设置线段中点的id，实际上就是确定点与点的连接顺序
		//polyline是按照polyline中的点索引顺序依次连接起来的，而非是point中的点索引顺序
		polyLine->GetPointIds()->SetId(i, i); //第一个参数是polyline中的点索引，第二个参数是point中的点索引
	}
	//创建元胞数组以存储多段线
	vtkSmartPointer<vtkCellArray> cells = vtkSmartPointer<vtkCellArray>::New();
	cells->InsertNextCell(polyLine);
	//创建多元数据对象，此处用于保存多段线
	vtkSmartPointer<vtkPolyData> polyData = vtkSmartPointer<vtkPolyData>::New();
	//加入点
	polyData->SetPoints(points);
	//加入线连接方式，它会将点按照它的方式连接成多段线
	polyData->SetLines(cells);
	//设置Actor和映射器
	vtkSmartPointer<vtkPolyDataMapper> mapper = vtkSmartPointer<vtkPolyDataMapper>::New();
	mapper->SetInputData(polyData);
	vtkSmartPointer<vtkActor> actor = vtkSmartPointer<vtkActor>::New();
	actor->SetMapper(mapper);
	actor->GetProperty()->SetColor(colors->GetColor3d("Tomato").GetData());
	//设置渲染器，渲染窗口和交互器
	vtkSmartPointer<vtkRenderer> renderer = vtkSmartPointer<vtkRenderer>::New();
	vtkSmartPointer<vtkRenderWindow> renderWindow = vtkSmartPointer<vtkRenderWindow>::New();
	renderWindow->SetWindowName("PolyLine");
	renderWindow->AddRenderer(renderer);
	vtkSmartPointer<vtkRenderWindowInteractor> renderWindowInteractor = vtkSmartPointer<vtkRenderWindowInteractor>::New();
	renderWindowInteractor->SetRenderWindow(renderWindow);
	renderer->AddActor(actor);
	renderer->SetBackground(colors->GetColor3d("DarkOliveGreen").GetData());
	renderWindow->Render();
	renderWindowInteractor->Start();
	return EXIT_SUCCESS;
}
