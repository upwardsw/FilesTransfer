#include <tchar.h>
#include <GL/glut.h>
#include <cstdlib>
 
#pragma comment( lib, "opengl32.lib" )   
#pragma comment( lib, "glu32.lib" )     
#pragma comment( lib, "glut32.lib" )     
 
void LineDDA(int x1,int y1,int x2,int y2)
{
    float x, y, dx, dy;
    int k,i;
    if(abs(x2-x1)>=abs(y2-y1))
    {
        k=abs(x2-x1);
    }
    else
    {
        k=abs(y2-y1);
    }
    dx=(float)(x2-x1)/k;
    dy=(float)(y2-y1)/k;
    x=(float)(x1);
    y=(float)(y1);
    for(i=0;i<k; i++)
    {
        glPointSize(2);
        glBegin (GL_POINTS);
        glColor3f (1.0f, 0.0f, 0.0f);
        glVertex2i ((int)(x+0.5),(int)(y+0.5));
        glEnd ();
        x+=dx;
        y+=dy;
    }  
} 
 
void RenderScene(void)
{
    glClear(GL_COLOR_BUFFER_BIT);
 
    glBegin(GL_LINES);
    glColor3f (0.0f, 0.0f, 0.0f);
    glVertex2f(100.0f,50.0f);
    glVertex2f(100.0f,150.0f);
    glEnd();
 
    glBegin(GL_LINES);
    glColor3f (0.0f, 0.0f, 0.0f);
    glVertex2f(50.0f,100.0f);
    glVertex2f(150.0f,100.0f);
    glEnd();
 
    LineDDA(50,50,150,150);
    LineDDA(50, 150, 150,50);
    glFlush();
}
void ChangeSize(GLsizei w,GLsizei h)
{
    if(h==0)
    {
        h=1;
    }
    glViewport(0,0,w,h);
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
 
    if(w<=h)
    {
        glOrtho(0.0f,250.0f,0.0f,250.0f*h/w,1.0f,-1.0f);
    }
    else
    {
        glOrtho(0.0f,250.0f*w/h,0.0f,250.0f,1.0f,-1.0f);
    }
 
    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();
 
}
 
void Init(void)
{
    glClearColor(1.0f,1.0f,1.0f,0.0f);
    glShadeModel(GL_FLAT);
}
 
int _tmain(int argc, _TCHAR* argv[])
{
    glutInitDisplayMode(GLUT_RGB | GLUT_SINGLE);
    glutCreateWindow("DDA算法画直线");
    Init();
    glutDisplayFunc(RenderScene);
    glutReshapeFunc(ChangeSize);
    glutMainLoop();
    return 0;
}