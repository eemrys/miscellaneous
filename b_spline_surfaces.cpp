#define GL_SILENCE_DEPRECATION

#include <iostream>
#include <stdio.h>
#include <OpenGL/gl.h>
#include <OpenGl/glu.h>
#include <GLUT/glut.h>

GLfloat ctlarray[8][2][4] = {
                            -0.8, 0.4, 0, 1.0,
                            -0.8, 0.4, 1, 1.0,
                             -0.55, 0.9, 0.0, 1 ,
                             -0.55, 0.9, 1.0, 1 ,
                             -0.3, 0.4, 0.0, 1,
                             -0.3, 0.4, 1.0, 1,
                             -0.05, 0.9, 0.0, 1 ,
                             -0.05, 0.9, 1.0, 1 ,
                             0.2, 0.4, 0.0, 1,
                             0.2, 0.4, 1.0, 1,
                             0.45, 0.9, 0.0, 1,
                             0.45, 0.9, 1.0, 1,
                             0.7, 0.4, 0.0, 1,
                             0.7, 0.4, 1.0, 1,
                            0.95, 0.9, 1.0, 1,
                            0.95, 0.9, 1.0, 1 };

GLfloat TexP2[] = { 0,0,1,0};
GLubyte  TexI[] = { 255,0,0,
                    255,153,51,
                    255,255,0,
                    0,255,0,
                    51,204,255,
                    0,0,255,
                    153,0,204 };
GLfloat texpts[2][2][2] = { 0,0,0,2,2,0,2,2 };
GLUnurbsObj* theNurb;

void init() {
    glClearColor(0.5, 0.5, 0.5, 1);
    theNurb = gluNewNurbsRenderer();
    glEnable(GL_DEPTH_TEST);
    gluNurbsProperty(theNurb, GLU_SAMPLING_TOLERANCE, 25.0);
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1);
    glTexParameterf(GL_TEXTURE_1D, GL_TEXTURE_MAG_FILTER, GL_NEAREST);
    glTexParameterf(GL_TEXTURE_1D, GL_TEXTURE_MIN_FILTER, GL_NEAREST);
    glTexImage1D(GL_TEXTURE_1D, 0, 3, 7, 0, GL_RGB, GL_UNSIGNED_BYTE, TexI);
    glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL);
    glEnable(GL_TEXTURE_1D);
}

void Display() {
    GLfloat knot[] = { 0, 1, 2, 3, 4, 5, 6, 7, 8, 9 };
    GLfloat knot1[] = { 0, 0, 1, 1 };
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
    glRotatef(-0.1, 0.1, -0.1, 0.0);
    glEnable(GL_TEXTURE_GEN_S);
    glTexGeni(GL_S, GL_TEXTURE_GEN_MODE, GL_OBJECT_LINEAR);
    glTexGenfv(GL_S, GL_OBJECT_PLANE, TexP2);
    glMap2f(GL_MAP2_TEXTURE_COORD_1, 0, 1, 2, 2, 0, 1, 4, 2, &texpts[0][0][0]);
    glEnable(GL_MAP2_TEXTURE_COORD_1);
    gluBeginSurface(theNurb);
    gluNurbsSurface(theNurb,
        10, knot,
        4, knot1,
        2 * 4,
        4,
        &ctlarray[0][0][0],
        4, 2,
        GL_MAP2_VERTEX_4);
    gluEndSurface(theNurb);
    glutPostRedisplay();
    glutSwapBuffers();
}

int main(int argc, char** argv) {
    glutInit(&argc, argv);
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH);
    glutInitWindowSize(480, 480);
    glutInitWindowPosition(100, 100);
    glutCreateWindow("  ");
    init();
    glutDisplayFunc(Display);
    glutMainLoop();
}
