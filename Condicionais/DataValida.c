#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#include <time.h>
int main(void)
{ 
int dia,mes,ano;
scanf("%d %d %d",&dia,&mes,&ano);
if(ano>=1900 && ano<=2100)
{
switch (mes)

{
case 1:
  if(dia<=31&&dia>=1){printf("valida");}
  else
    {
     printf("invalida");
    }
  break;
case 2:
  if(ano%400==0 || (ano%4 == 0 && ano%100 != 0))
  {
    if(dia<=29&&dia>=1){printf("valida");}
    else
    {
     printf("invalida");
    }
  }
  else 
  {
    if (dia<=28&&dia>=1)
    {
     printf("valida");
    }
    else
    {
     printf("invalida");
    }
  }
  break;
case 3:
  if(dia<=31&&dia>=1)
  {
    printf("valida");
  }
  else
  {
    printf("invalida");
  }
  
  break;
case 4:
  if(dia<=30&&dia>=1){printf("valida");}
  else
    {
     printf("invalida");
    }
  break;
case 5:
  if(dia<=31&&dia>=1){printf("valida");}
  else
    {
     printf("invalida");
    }
  break;
case 6:
  if(dia<=30&&dia>=1){printf("valida");}
  else
    {
     printf("invalida");
    }
  break;
case 7:
  if(dia<=31&&dia>=1){printf("valida");}
  else
    {
     printf("invalida");
    }
  break;
case 8:
  if(dia<=31&&dia>=1){printf("valida");}
  else
    {
     printf("invalida");
    }
  break;
case 9:
  if(dia<=30&&dia>=1){printf("valida");}
  else
    {
     printf("invalida");
    }
  break;
case 10:
  if(dia<=31&&dia>=1){printf("valida");}
  else
    {
     printf("invalida");
    }
  break;
case 11:
  if(dia<=30&&dia>=1){printf("valida");}
  else
    {
     printf("invalida");
    }
  break;
case 12:
  if(dia<=31&&dia>=1){printf("valida");}
  else
    {
     printf("invalida");
    }
  break;


default:
printf("invalida");
  break;
}
}
else
{printf("invalida");}
  return 0;
}
