#-------------------------------------------------------------------------------
# Name:        newton
# Author:      d.fathi
# Created:     01/03/2015
# Update:      04/10/2021
# Copyright:   (c) pyams
# Web:         www.PyAMS.org
# Licence:     free
# info:        solving systems of nonlinear equations newton raphson method
#-------------------------------------------------------------------------------

from math import fabs,sqrt
from armijo import armijo
from option import simulationOption


#-------------------------------------------------------------------------------
# def norm: the norm of a vector
#-------------------------------------------------------------------------------

def norm(x):
    return sqrt(sum(i**2 for i in x))


#-------------------------------------------------------------------------------
# def solve_LU: solving a system with an LU-Factorization
#-------------------------------------------------------------------------------

def solve_LU(at,bt,n):
    a= [[0 for j in range(n)] for i in range(n)];
    b= [0 for i in range(n)];
    v= [0 for i in range(n)];
    indx = [0 for i in range(n)];
    d = 1;
    tiny = 1e-20;
    imax=0;

    for i in range(n):
        for j in range(n):
            a[i][j] =at[i][j];
        b[i] =bt[i];

    for  i in  range(n):
         big = 0.0;
         for  j in  range(n):
             temp = abs(a[i][j]);
             if (temp > big):
                 big = temp;
         if (big != 0.0):
            v[i] = 1.0 / big;
         else:
            v[i] = 100000000.0;

    for  j in  range(n):
        for  i in  range(j):
             sum_ = a[i][j];
             for  k in  range(i):
                sum_ = sum_ - (a[i][k]*a[k][j]);
             a[i][j] = sum_;

        big = 0.0;
        for  i in  range(j,n):
         sum_ = a[i][j];
         for  k in  range(j):
                sum_ = sum_ - (a[i][k] * a[k][j]);
         a[i][j] = sum_;
         dum = v[i] * abs(sum_);
         if (dum >= big):
             big = dum;
             imax = i;
        if (j != imax):
            for  k in  range(n):
                dum = a[imax][k];
                a[imax][k] = a[j][k];
                a[j][k] =dum;
            d = -d;
            v[imax] = v[j];

        indx[j] = imax;

        if (a[j][j]== 0.0):
            a[j][j] = tiny;

        if (j != n):
            dum =1.0/a[j][j];
            for  i in  range(j+1,n):
                a[i][j] = a[i][j] * dum;

    ii = -1;
    for  i in  range(n):
        ip = indx[i];
        sum_ = b[ip];
        b[ip] = b[i];
        if (ii != -1):
            for  j in  range(ii,i):
                sum_ = sum_ -a[i][j]*b[j];
        else:
            if (sum_ !=0.0):
                ii = i;
        b[i]=sum_;

    i=n-1;
    while (i >= 0):
        sum_ = b[i];
        for  j in  range(i+1,n):
             sum_ = sum_ - a[i][j]*b[j];
        if (a[i][i] != 0.0):
             b[i]=sum_/a[i][i];
        else:
             b[i]=sum_/tiny;
        i=i-1;
    return b;
'''
    for i in range(0,n):
        for j in range(0,n):
            a[i][j] =at[i][j];
        b[i] =bt[i];

    for  i in  range(0,n):
         big = 0.0;
         for  j in  range(0,n):
             temp = abs(a[i][j]);
             if (temp > big):
                 big = temp;
         if (big != 0.0):
            v[i] = 1.0 / big;
         else:
            v[i] = 100000000.0;

    for  j in  range(0,n):
        for  i in  range(0,j):
             sum_ = a[i][j];
             for  k in  range(0,i):
                sum_ = sum_ - (a[i][k]*a[k][j]);
             a[i][j] = sum_;

        big = 0.0;
        for  i in  range(0,n):
         sum_ = a[i][j];
         for  k in  range(0,j):
                sum_ = sum_ - (a[i][k] * a[k][j]);
         a[i][j] = sum_;
         dum = v[i] * abs(sum_);
         if (dum >= big):
             big = dum;
             imax = i;
        if (j != imax):
            for  k in  range(0,n):
                dum = a[imax][k];
                a[imax][k] = a[j][k];
                a[j][k] =dum;
            d = -d;
            v[imax] = v[j];

        indx[j] = imax;

        if (a[j][j]== 0.0):
            a[j][j] = tiny;

        if (j != n):
            dum =1.0/a[j][j];
            for  i in  range(j+1,n):
                a[i][j] = a[i][j] * dum;

    ii = -1;
    for  i in  range(0,n):
        ip = indx[i];
        sum_ = b[ip];
        b[ip] = b[i];
        if (ii != -1):
            for  j in  range(ii,i):
                sum_ = sum_ -a[i][j]*b[j];
        else:
            if (sum_ !=0.0):
                ii = i;
        b[i]=sum_;
    print(b)
    print(a)
    i=n-1;
    while (i >= 0):
        sum_ = b[i];
        for  j in  range(i+1,n):
             sum_ = sum_ - a[i][j]*b[j];
        if (a[i][i] != 0.0):
             b[i]=sum_/a[i][i];
        else:
             b[i]=sum_/tiny;
        i=i-1;
    return b;

a=[[1.0,2.0],[3.0,4.0]]
b=[3.0,7.0]
print(solve_LU(a,b,2))
'''
#-------------------------------------------------------------------------------
# def jac: Jacobian matrix
#-------------------------------------------------------------------------------
def jac(x,f,n):
    delta=1e-6;
    J= [[0 for j in range(n)] for i in range(n)];
    f2= [0 for i in range(n)];
    f3= [0 for i in range(n)];
    for i in range(0,n):
        tmp= x[i];
        x[i]= tmp+delta;
        f2=f(x);
        x[i]= tmp-delta;
        f3=f(x);
        x[i]= tmp;
        for k in range(0,n):
          J[k][i]=(f2[k]-f3[k])/(2*delta);
    return J


#-------------------------------------------------------------------------------
# def convergence: convergence systems of nonlinear equations
#-------------------------------------------------------------------------------
def convergence(xo,x,y,n,vlen,vles):
    r=True
    if (len(xo)!=len(x)):
        return False
    else:
        for i in range(n):
            if (i < vlen):
              r=r and (abs(xo[i]-x[i])<=(simulationOption.reltol*max(abs(xo[i]),abs(x[i]))+simulationOption.vntol))
            else:
              r=r and (abs(xo[i]-x[i])<=(simulationOption.reltol*max(abs(xo[i]),abs(x[i]))+simulationOption.abstol))

    #r=r and (abs(sum(y(x)))<1e-10)
    return r


#-------------------------------------------------------------------------------
# def solven: solving systems of nonlinear equations by newton raphson method
#-------------------------------------------------------------------------------

def solven(x,y):
 ii=0;
 xo=[]

 n,vlen,vles=simulationOption.size,simulationOption.len,simulationOption.les

 while(not(convergence(xo,x,y,n-1,vlen,vles))):
      xo=[]
      xo+=x
      J=jac(x,y,n-1);
      F=y(x);
      dx=solve_LU(J,F,n-1);
      ii=ii+1;
      x=armijo(dx,x,F,simulationOption.ITLC,y,n-1);
      if ii > simulationOption.itl1:
          print('Error of convergence: ',ii,':',fabs(sum(y(x))))
          return x,False

 xo=[]
 ii=0;

 '''
 while(not(convergence(xo,x,y,n-1,vlen,vles))):
      xo=[]
      xo+=x
      J=jac(x,y,n-1);
      F=y(x);
      dx=solve_LU(J,F,n-1);
      ii=ii+1;
      for i in range(0,n-1):
        x[i]= x[i]-0.5*dx[i];
      if ii > simulationOption.itl1:
          print('Error of convergence: ',ii,':',fabs(sum(y(x))))
          return x,False
 #print("ii="+str(ii))
 '''
 return x,True;


'''
from scipy.optimize import  fsolve,newton
from numpy import ndarray
def solveng(x,y):
    r=fsolve(y,x);
    a=ndarray.tolist(r);
    return solveng(a,y);
'''




