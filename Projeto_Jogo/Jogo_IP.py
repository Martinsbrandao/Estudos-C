#include "raylib.h"
#include <stdlib.h>
 
#define VELOCIDADE_PULO_INICIAL 580.0
#define G 1260
#define ESPACO_ENTRE_FLUTUANTES 320
#define LARGURA_MINIMA_FLUTUANTES 220
#define LARGURA_MAXIMA_FLUTUANTES 280
#define ESPESSURA_FLUTUANTES 40
#define MULTIPLICA_VELOCIDADE_CORRER 1.2
#define MULTIPLICA_VELOCIDADE_PULO 1.1
#define MULTIPLICA_GRAVIDADE 1.2
#define MULTIPLICA_VELOCIDADE_INIMIGO 1.1
#define MINIMO_FLUTUTANTES 40
#define MAXIMO_FLUTUANTES 60
#define MAX_DIST_VERT_FLUTUANTES 62
#define ALTURA_CONE 75
#define VELOCIDADE_INIMIGO1 3
#define VELOCIDADE_INIMIGO3 4
 
typedef struct{
  Vector2 posicao;
  float velocidade;
  bool taNoChao;
  Texture2D textSprite;
} Jogador;
 
typedef struct{
  Texture2D textura;
  Vector2 posicao;
} Plataforma;
 
void reeditaCenario(Plataforma **flutuantes, Plataforma *platPrincI, Plataforma *platPrincII, int *qtdFlutuantes);

void desenhaSecundarios(Texture2D *textPlacar, Texture2D *textCenario, int xCenario, int nivel, float contPontos, Jogador *player);

void desenhaPrincipais2D(Plataforma *platPrincI, Plataforma *platPrincII, Rectangle *obstaculos, Texture2D *textCone, Plataforma *flutuantes, int qtdFlutuantes);

void desenhaInimigos(int *idxInimigo, Rectangle *obstaculos, Texture2D *inimigo1, Texture2D *inimigo2, Texture2D *inimigo3, Texture2D *inimigo4, float *xInimigo1, float *xInimigo3, float multInimigo);

void atualizaJogador(Sound *muscapulo, Jogador *player, bool *voltouProZero, Plataforma *flutuantes, int qtdFlutuantes, Plataforma *platPrincI, Plataforma *platPrincII, float delta, float multVeloc, float velocidadePulo, float gravidade, float multPulo);

void desenhaJogador(int *acrescimoHitboxJogador, int *idxPulando, int *idxCorrendo, Jogador *player, int *alturaIdeal, int *larguraIdeal, Texture2D *move1, Texture2D *move2, Texture2D *move3, Texture2D *move4, Texture2D *move5, Texture2D *move6, Texture2D *move7, Texture2D *jump);

void carregarTexturasJogadores(Texture2D *move1, Texture2D *move2, Texture2D *move3, Texture2D *move4, Texture2D *move5, Texture2D *move6, Texture2D *move7, Texture2D *jump, Texture2D *inimigo1, Texture2D *inimigo2, Texture2D *inimigo3, Texture2D *inimigo4);

void refazContexto(bool *voltouProZero, float *multVeloc, float *gravidade, float *multPulo, int *nivel, float *xInimigo1, float *xInimigo3, int *xCenario, int *idxInimigo, float *multInimigo);

void perdeuJogo(Sound *muscajogo, int *idxPulando, int *idxCorrendo, float *multVeloc, float *velocidadePulo, float *gravidade, float *multPulo, int *nivel, float *contPontos, Jogador *player, float *xInimigo1, float *xInimigo3, Texture2D *textGameOver, int *xCenario, int *idxInimigo, float *multInimigo);

int bateu(Rectangle *hitbox, Rectangle *obstaculos);

void fecharJogo(Plataforma *flutuantes, Sound *muscamenu, Sound *muscapulo, Sound *muscajogo, Texture2D *textPlacar, Texture2D *texturaMenu, Texture2D *textGameOver, Plataforma *platPrincI, Plataforma *platPrincII, Texture2D *textCenario, Texture2D *textCone, int qtdFlutuantes, Texture2D *move1, Texture2D *move2, Texture2D *move3, Texture2D *move4, Texture2D *move5, Texture2D *move6, Texture2D *move7, Texture2D *inimigo1, Texture2D *inimigo2, Texture2D *inimigo3, Texture2D *inimigo4, Texture2D *jump);
 
int main(void){
    
 int larguraDaTela = 1000;
 int alturaDaTela = 600;
 InitWindow(larguraDaTela, alturaDaTela, "Rumo ao Hexa!");
 
 int idxCorrendo = 0;
 int idxPulando = 0;
 int idxInimigo = 0;
 bool tanoMenu = true;
 float delta = 0;
 float multVeloc = 1;
 float velocidadePulo = VELOCIDADE_PULO_INICIAL;
 float gravidade = G;
 float multPulo = 1;
 int nivel = 1;
 float contPontos = 0;
 int alturaIdeal = 0;
 int larguraIdeal = 0;
 int xCenario = 0;
 int acrescimoHitboxJogador = 0;
 bool voltouProZero = false;
 
 Plataforma *flutuantes = NULL;
 int qtdFlutuantes = GetRandomValue(MINIMO_FLUTUTANTES, MAXIMO_FLUTUANTES);
 flutuantes = (Plataforma *) realloc(flutuantes, qtdFlutuantes * sizeof(Plataforma));
 if (flutuantes == NULL) exit(1);
 
 Jogador player = { 0 };
 player.posicao.x = 100;
 player.posicao.y = 320;
 player.velocidade = 0;
 player.taNoChao = false;
 Texture2D move1, move2, move3, move4, move5, move6, move7, inimigo1, inimigo2, inimigo3, inimigo4, jump;
 
 Plataforma platPrincI = { 0 };
 Plataforma platPrincII = { 0 };
 
 float xInimigo1 = 3300;
 float xInimigo3 = 7200;
 float multInimigo = 1;
 
 InitAudioDevice();
 Sound musicajogo = LoadSound("assets/sound/muscajogo.wav");
 Sound musicamenu = LoadSound("assets/sound/muscamenu.wav");
 Sound sompulo = LoadSound("assets/sound/muscapulo.wav");
 
 bool MusicaMenuTaTocando = IsSoundPlaying(musicamenu);
 bool MusicaJogoTaTocando = IsSoundPlaying(musicajogo);
 
 Image cone = LoadImage("assets/cone.png");
 ImageResize(&cone, (int) ALTURA_CONE * 0.83, ALTURA_CONE);
 Texture2D textCone = LoadTextureFromImage(cone);
 UnloadImage(cone);
 
 Image iconePlacar = LoadImage("assets/placar.png");
 ImageResize(&iconePlacar, 30, 30);
 Texture2D textPlacar = LoadTextureFromImage(iconePlacar);
 UnloadImage(iconePlacar);
 
 Image menu = LoadImage("assets/menu_principal.png");
 ImageResize(&menu, 1000, 600);
 Texture2D texturaMenu = LoadTextureFromImage(menu);
 UnloadImage(menu);
 
 Image gameOver = LoadImage("assets/game_over.png");
 ImageResize(&gameOver, 1000, 600);
 Texture2D textGameOver = LoadTextureFromImage(gameOver);
 UnloadImage(gameOver);
 
 Image cenario = LoadImage("assets/cenario.png");
 Texture2D textCenario = LoadTextureFromImage(cenario);
 UnloadImage(cenario);
 
 carregarTexturasJogadores(&move1, &move2, &move3, &move4, &move5, &move6, &move7, &jump, &inimigo1, &inimigo2, &inimigo3, &inimigo4);
 reeditaCenario(&flutuantes, &platPrincI, &platPrincII, &qtdFlutuantes);
 
 Rectangle obstaculos[12] = { { 2000, 320 - textCone.height, textCone.width, textCone.height },
                              { 3000, 215, 100, 105},
                              { 5800, 320 - textCone.height, textCone.width, textCone.height },
                              { 7200, 215, 100, 105 },
                              { 7000, 320 - textCone.height, textCone.width, textCone.height },
                              { 8000, 320 - textCone.height, textCone.width, textCone.height },
                              { 9000, 320 - textCone.height, textCone.width, textCone.height },
                              { 3500, 320 - textCone.height, textCone.width, textCone.height },
                              { 9500, 320 - textCone.height, textCone.width, textCone.height },
                              { 4300, 320 - textCone.height, textCone.width, textCone.height },
                              { 10740, 320 - textCone.height, textCone.width, textCone.height },
                              { 7500, 320 - textCone.height, textCone.width, textCone.height } };
 
 int posYCamera = player.posicao.y - 80;
 Camera2D camera = { 0 };
 camera.target = (Vector2){ player.posicao.x + 260, posYCamera };
 camera.offset = (Vector2){ larguraDaTela/2.0f, alturaDaTela/2.0f };
 camera.rotation = 0.0f;
 camera.zoom = 1.0f;
 
 SetTargetFPS(60);
 
 PlaySound(musicamenu);
  
 while (!WindowShouldClose()){
  MusicaMenuTaTocando = IsSoundPlaying(musicamenu);
  MusicaJogoTaTocando = IsSoundPlaying(musicajogo);
 
  Rectangle hitbox = { player.posicao.x + acrescimoHitboxJogador, player.posicao.y - alturaIdeal, larguraIdeal, alturaIdeal };
  camera.target = (Vector2){ player.posicao.x + 260, posYCamera };
 
  if(tanoMenu && IsKeyPressed(KEY_ENTER)){
  
    StopSound(musicamenu);
    tanoMenu = false;
   
  }
 
  else if(tanoMenu){
      
   if(!MusicaMenuTaTocando) PlaySound(musicamenu);
  
   BeginDrawing();
    DrawTexture(texturaMenu, 0, 0, WHITE);
   EndDrawing();
  
  }
  
  else{
      if(!MusicaJogoTaTocando) PlaySound(musicajogo);
 
      if (bateu(&hitbox, obstaculos) || player.posicao.y >= 600){
         perdeuJogo(&musicajogo, &idxPulando, &idxCorrendo, &multVeloc, &velocidadePulo, &gravidade, &multPulo, &nivel, &contPontos, &player, &xInimigo1, &xInimigo3, &textGameOver, &xCenario, &idxInimigo, &multInimigo);
      }
      else{
          xCenario -= 1;
        
            BeginDrawing();
              
               desenhaSecundarios(&textPlacar, &textCenario, xCenario, nivel, contPontos, &player);
               
                BeginMode2D(camera);
                
                   desenhaJogador(&acrescimoHitboxJogador, &idxPulando, &idxCorrendo, &player, &alturaIdeal, &larguraIdeal, &move1, &move2, &move3, &move4, &move5, &move6, &move7, &jump);
                   desenhaPrincipais2D(&platPrincI, &platPrincII, obstaculos, &textCone, flutuantes, qtdFlutuantes);
                   desenhaInimigos(&idxInimigo, obstaculos, &inimigo1, &inimigo2, &inimigo3, &inimigo4, &xInimigo1, &xInimigo3, multInimigo);
                    
                EndMode2D();
                 
            EndDrawing();
      
          delta = GetFrameTime();
          atualizaJogador(&sompulo, &player, &voltouProZero, flutuantes, qtdFlutuantes, &platPrincI, &platPrincII, delta, multVeloc, velocidadePulo, gravidade, multPulo);
 
          contPontos += GetFrameTime();
      
          if (voltouProZero){
            reeditaCenario(&flutuantes, &platPrincI, &platPrincII, &qtdFlutuantes);
            refazContexto(&voltouProZero, &multVeloc, &gravidade, &multPulo, &nivel, &xInimigo1, &xInimigo3, &xCenario, &idxInimigo, &multInimigo);
          }
      }
  }
 }
 
  fecharJogo(flutuantes, &musicamenu, &sompulo, &musicajogo, &textPlacar, &texturaMenu, &textGameOver, &platPrincI, &platPrincII, &textCenario, &textCone, qtdFlutuantes, &move1, &move2, &move3, &move4, &move5, &move6, &move7, &inimigo1, &inimigo2, &inimigo3, &inimigo4, &jump);
  CloseAudioDevice();
  CloseWindow();
  
  return 0;
  
}
 
 
 
 
 
 
void reeditaCenario(Plataforma **flutuantes, Plataforma *platPrincI, Plataforma *platPrincII, int *qtdFlutuantes){
 
 float xAnterior = 11000;
 float yAnterior = 320;
 int i = 0;
 
 for (int j = 0; j < *qtdFlutuantes; j++) UnloadTexture((*flutuantes)[j].textura);
 
 *qtdFlutuantes = GetRandomValue(MINIMO_FLUTUTANTES, MAXIMO_FLUTUANTES);
 Plataforma *tmp = (*flutuantes);
 (*flutuantes) = (Plataforma *) realloc((*flutuantes), (*qtdFlutuantes) * sizeof(Plataforma));
 
 if ((*flutuantes) == NULL){
    free(tmp);
    exit(1);
 }
 
 for (i = 0; i < *qtdFlutuantes; i++){
    Image plataforma = LoadImage("assets/plataforma1.png");
    ImageResize(&plataforma, GetRandomValue(LARGURA_MINIMA_FLUTUANTES, LARGURA_MAXIMA_FLUTUANTES), ESPESSURA_FLUTUANTES);
    (*flutuantes)[i].textura = LoadTextureFromImage(plataforma);
    UnloadImage(plataforma);
   
    (*flutuantes)[i].posicao.x = xAnterior + ESPACO_ENTRE_FLUTUANTES;
    (*flutuantes)[i].posicao.y = GetRandomValue(yAnterior - MAX_DIST_VERT_FLUTUANTES, yAnterior + MAX_DIST_VERT_FLUTUANTES);
  
    if ((*flutuantes)[i].posicao.y <= 0){
        (*flutuantes)[i].posicao.y = 40;
    }
    else if ((*flutuantes)[i].posicao.y >= 600){
        (*flutuantes)[i].posicao.y = 570;
    }
  
    xAnterior = (*flutuantes)[i].posicao.x + (*flutuantes)[i].textura.width;
 }
 
 int xPlatII = (*flutuantes)[i - 1].posicao.x + (*flutuantes)[i - 1].textura.width + ESPACO_ENTRE_FLUTUANTES;
 
 Image image = LoadImage("assets/plataforma_principal.png");
 ImageResize(&image, image.width, 280);
 
 platPrincII->textura = LoadTextureFromImage(image);
 platPrincII->posicao.x = xPlatII;
 platPrincII->posicao.y = 320;
 
 platPrincI->textura = LoadTextureFromImage(image);
 platPrincI->posicao.x = 360 - 2000;
 platPrincI->posicao.y = 320;
 
}
 
void refazContexto(bool *voltouProZero, float *multVeloc, float *gravidade, float *multPulo, int *nivel, float *xInimigo1, float *xInimigo3, int *xCenario, int *idxInimigo, float *multInimigo){
  
 *voltouProZero = false;
 *multVeloc *= MULTIPLICA_VELOCIDADE_CORRER;
 *gravidade *= MULTIPLICA_GRAVIDADE;
 *multPulo *= MULTIPLICA_VELOCIDADE_PULO;
 *multInimigo *= MULTIPLICA_VELOCIDADE_INIMIGO;
 (*nivel)++;
 *xInimigo1 = 3300;
 *xInimigo3 = 7200;
 *xCenario = 0;
 *idxInimigo = 0;
 
}
 
void atualizaJogador(Sound *muscapulo, Jogador *player, bool *voltouProZero, Plataforma *flutuantes, int qtdFlutuantes, Plataforma *platPrincI, Plataforma *platPrincII, float delta, float multVeloc, float velocidadePulo, float gravidade, float multPulo){
  
  (*player).posicao.x += 8.0 * multVeloc;
  
  if ((*player).posicao.x >= platPrincII->posicao.x + 2000){
     *voltouProZero = true;
     (*player).posicao.x = 300;
  }
  
  if (IsKeyDown(KEY_SPACE) && player->taNoChao)
  {
     player->velocidade = -velocidadePulo * multPulo;
     player->taNoChao = false;
     PlaySound(*muscapulo);
  }
  
  int hitObstacle = 0;
  
  for (int i = 0; i < qtdFlutuantes; i++)
  {
    if (flutuantes[i].posicao.x <= (*player).posicao.x + player->textSprite.width &&
        flutuantes[i].posicao.x + flutuantes[i].textura.width >= (*player).posicao.x &&
        flutuantes[i].posicao.y >= (*player).posicao.y &&
        flutuantes[i].posicao.y <= (*player).posicao.y + player->velocidade * delta)
    {
        hitObstacle = 1;
        player->velocidade = 0.0f;
        (*player).posicao.y = flutuantes[i].posicao.y;
    }
  }

  if (platPrincI->posicao.x <= (*player).posicao.x &&
     platPrincI->posicao.x + platPrincI->textura.width >= (*player).posicao.x &&
     platPrincI->posicao.y >= (*player).posicao.y &&
     platPrincI->posicao.y <= (*player).posicao.y + player->velocidade * delta)
  {
    hitObstacle = 1;
    player->velocidade = 0.0f;
    (*player).posicao.y = platPrincI->posicao.y;
  }
  else if(platPrincII->posicao.x <= (*player).posicao.x &&
         platPrincII->posicao.x + platPrincII->textura.width >= (*player).posicao.x &&
         platPrincII->posicao.y >= (*player).posicao.y &&
         platPrincII->posicao.y <= (*player).posicao.y + player->velocidade * delta)
  {
    hitObstacle = 1;
    player->velocidade = 0.0f;
    (*player).posicao.y = platPrincI->posicao.y;
  }
 
  if (!hitObstacle)
  {
    (*player).posicao.y += player->velocidade * delta;
    player->velocidade += gravidade * delta;
    player->taNoChao = false;
  }
  else player->taNoChao = true;
 
}

void perdeuJogo(Sound *muscajogo, int *idxPulando, int *idxCorrendo, float *multVeloc, float *velocidadePulo, float *gravidade, float *multPulo, int *nivel, float *contPontos, Jogador *player, float *xInimigo1, float *xInimigo3, Texture2D *textGameOver, int *xCenario, int *idxInimigo, float *multInimigo){
 
  BeginDrawing();
      DrawTexture(*textGameOver, 0, 0, WHITE);
      StopSound(*muscajogo);
      if (IsKeyPressed(KEY_Q)){
         
          *multVeloc = 1;
          *velocidadePulo = VELOCIDADE_PULO_INICIAL;
          *gravidade = G;
          *multPulo = 1;
          *nivel = 1;
          *contPontos = 0;
          player->posicao.x = 360;
          player->posicao.y = 320;
          player->velocidade = 0;
          player->taNoChao = false;
          *idxCorrendo = 0;
          *idxPulando = 0;
          *idxInimigo = 0;
          *xCenario = 0;
          *xInimigo1 = 3300;
          *xInimigo3 = 7200;
          *multInimigo = 1;
      }
  EndDrawing();
 
}

int bateu(Rectangle *hitbox, Rectangle *obstaculos){
  
  for (int i = 0; i < 12; i++){
    if (CheckCollisionRecs(*hitbox, obstaculos[i])) return 1;
  }
  return 0;
 
}

void carregarTexturasJogadores(Texture2D *move1, Texture2D *move2, Texture2D *move3, Texture2D *move4, Texture2D *move5, Texture2D *move6, Texture2D *move7, Texture2D *jump, Texture2D *inimigo1, Texture2D *inimigo2, Texture2D *inimigo3, Texture2D *inimigo4){
  
  int altura = 0;
  int largura = 0;
  
  Image image = LoadImage("assets/sprites/move1.png");
  altura = (int) image.height / 3;
  largura = (int) (image.width / image.height) * altura;
  ImageResize(&image, largura, altura);
  *move1 = LoadTextureFromImage(image);
  
  image = LoadImage("assets/sprites/move2.png");
  altura = (int) image.height / 3;
  largura = (int) (image.width / image.height) * altura;
  ImageResize(&image, largura, altura);
  *move2 = LoadTextureFromImage(image);
  
  image = LoadImage("assets/sprites/move3.png");
  altura = (int) image.height / 3;
  largura = (int) (image.width / image.height) * altura;
  ImageResize(&image, largura, altura);
  *move3 = LoadTextureFromImage(image);
  
  image = LoadImage("assets/sprites/move4.png");
  altura = 87;
  largura = 56;
  ImageResize(&image, largura, altura);
  *move4 = LoadTextureFromImage(image);
  
  image = LoadImage("assets/sprites/move5.png");
  altura = 87;
  largura = 42;
  ImageResize(&image, largura, altura);
  *move5 = LoadTextureFromImage(image);
  
  image = LoadImage("assets/sprites/move6.png");
  altura = (int) image.height / 3;
  largura = (int) (image.width / image.height) * altura;
  ImageResize(&image, largura, altura);
  *move6 = LoadTextureFromImage(image);
  
  image = LoadImage("assets/sprites/move7.png");
  altura = (int) image.height / 3;
  largura = (int) (image.width / image.height) * altura;
  ImageResize(&image, largura, altura);
  *move7 = LoadTextureFromImage(image);
  
  image = LoadImage("assets/sprites/jump.png");
  altura = 100;
  largura = 64;
  ImageResize(&image, largura, altura);
  *jump = LoadTextureFromImage(image);
 
  image = LoadImage("assets/sprites/inimigo1.png");
  altura = (int) image.height / 2.8;
  largura = (int) (image.width / image.height) * altura;
  ImageResize(&image, largura, altura);
  *inimigo1 = LoadTextureFromImage(image);
 
  image = LoadImage("assets/sprites/inimigo2.png");
  altura = (int) image.height / 2.8;
  largura = (int) (image.width / image.height) * altura;
  ImageResize(&image, largura, altura);
  *inimigo2 = LoadTextureFromImage(image);
 
  image = LoadImage("assets/sprites/inimigo3.png");
  altura = (int) image.height / 2.5;
  largura = (int) (image.width / image.height) * altura;
  ImageResize(&image, largura, altura);
  *inimigo3 = LoadTextureFromImage(image);
 
  image = LoadImage("assets/sprites/inimigo4.png");
  altura = (int) image.height / 2.5;
  largura = (int) (image.width / image.height) * altura;
  ImageResize(&image, largura, altura);
  *inimigo4 = LoadTextureFromImage(image);
  
  UnloadImage(image);
 
}

void desenhaJogador(int *acrescimoHitboxJogador, int *idxPulando, int *idxCorrendo, Jogador *player, int *alturaIdeal, int *larguraIdeal, Texture2D *move1, Texture2D *move2, Texture2D *move3, Texture2D *move4, Texture2D *move5, Texture2D *move6, Texture2D *move7, Texture2D *jump){
  
  if (player->taNoChao){
      if (*idxCorrendo >= 0 && *idxCorrendo <= 3){
          *alturaIdeal = move1->height;
          *larguraIdeal = move1->width;
          *acrescimoHitboxJogador = 0;
          DrawTexture(*move1, player->posicao.x, player->posicao.y - *alturaIdeal, WHITE);
          player->textSprite = *move1;
      }
      else if (*idxCorrendo >= 4 && *idxCorrendo <= 7){
          *alturaIdeal = move2->height;
          *larguraIdeal = move2->width;
          *acrescimoHitboxJogador = 0;
          DrawTexture(*move2, player->posicao.x, player->posicao.y - *alturaIdeal, WHITE);
          player->textSprite = *move2;
      }
      else if (*idxCorrendo >= 8 && *idxCorrendo <= 11){
          *alturaIdeal = move3->height;
          *larguraIdeal = move3->width;   
          *acrescimoHitboxJogador = 0;          
          DrawTexture(*move3, player->posicao.x, player->posicao.y - *alturaIdeal, WHITE);
          player->textSprite = *move3;
      }
      else if (*idxCorrendo >= 12 && *idxCorrendo <= 15){
          *alturaIdeal = move4->height;
          *larguraIdeal = move4->width + 18;
          *acrescimoHitboxJogador = 18;
          DrawTexture(*move4, player->posicao.x + 18, player->posicao.y - *alturaIdeal, WHITE);
          player->textSprite = *move4;
      }
      else if (*idxCorrendo >= 16 && *idxCorrendo <= 19){
          *alturaIdeal = move5->height;
          *larguraIdeal = move5->width + 18;
          *acrescimoHitboxJogador = 18;
          DrawTexture(*move5, player->posicao.x + 18, player->posicao.y - *alturaIdeal, WHITE);
          player->textSprite = *move5;
      }
      else if (*idxCorrendo >= 20 && *idxCorrendo <= 23){
          *alturaIdeal = move6->height;
          *larguraIdeal = move6->width;
          *acrescimoHitboxJogador = 0;
          DrawTexture(*move6, player->posicao.x, player->posicao.y - *alturaIdeal, WHITE);
          player->textSprite = *move6;
      }
      else if (*idxCorrendo >= 24 && *idxCorrendo <= 27){
          *alturaIdeal = move7->height;
          *larguraIdeal = move7->width;
          *acrescimoHitboxJogador = 0;
          DrawTexture(*move7, player->posicao.x, player->posicao.y - *alturaIdeal, WHITE);
          player->textSprite = *move7;
      }
      *idxCorrendo = (*idxCorrendo + 1) % 28;
      *idxPulando = 0;
  }
  else{
      *alturaIdeal = jump->height;
      *larguraIdeal = jump->width;
      *acrescimoHitboxJogador = 10;
      DrawTexture(*jump, player->posicao.x + *acrescimoHitboxJogador, player->posicao.y - *alturaIdeal, WHITE);
      player->textSprite = *jump;
      *idxCorrendo = 0;
  }
 
}
 
void desenhaSecundarios(Texture2D *textPlacar, Texture2D *textCenario, int xCenario, int nivel, float contPontos, Jogador *player){
  
  ClearBackground(WHITE);
  DrawTexture(*textCenario, xCenario, 0, WHITE);
 
  if (player->posicao.x <= 1500) DrawText(TextFormat("Nível %d", nivel), 450, 250, 50, (Color) { 253, 249, 0, 255 });
  
  DrawTexture(*textPlacar, 10, 18, WHITE);
  DrawText(TextFormat("%d", (int) contPontos), 52, 20, 30, YELLOW);
  if (contPontos <= 5) DrawText("Pressione espaço para desviar de obstáculos.", 15, 55, 28, YELLOW);
  
}
 
void desenhaPrincipais2D(Plataforma *platPrincI, Plataforma *platPrincII, Rectangle *obstaculos, Texture2D *textCone, Plataforma *flutuantes, int qtdFlutuantes){
  
  DrawTexture(platPrincI->textura, platPrincI->posicao.x, platPrincII->posicao.y, WHITE);
  DrawTexture(platPrincII->textura, platPrincII->posicao.x, platPrincII->posicao.y, WHITE);
 
   for (int r = 0; r < 12; r++){
       if (r != 1 && r != 3) DrawTexture(*textCone, obstaculos[r].x, obstaculos[r].y, WHITE);
   }
 
   for (int i = 0; i < qtdFlutuantes; i++){
      DrawTexture(flutuantes[i].textura, flutuantes[i].posicao.x, flutuantes[i].posicao.y, WHITE);
   }
  
}
 
void desenhaInimigos(int *idxInimigo, Rectangle *obstaculos, Texture2D *inimigo1, Texture2D *inimigo2, Texture2D *inimigo3, Texture2D *inimigo4, float *xInimigo1, float *xInimigo3, float multInimigo){
   *xInimigo1 -= VELOCIDADE_INIMIGO1 * multInimigo;
   *xInimigo3 -= VELOCIDADE_INIMIGO3 * multInimigo;
      
   if (*idxInimigo >= 0 && *idxInimigo <= 5){
       obstaculos[1].x = *xInimigo1 + 22;
       obstaculos[3].x = *xInimigo3 + 22;
       obstaculos[1].width = (*inimigo1).width - 38;
       obstaculos[3].width = (*inimigo1).width - 38;
       obstaculos[1].height = (*inimigo1).height;
       obstaculos[3].height = (*inimigo1).height;
       obstaculos[1].y = 320 - (*inimigo1).height;
       obstaculos[3].y = 320 - (*inimigo1).height;
      
       DrawTexture(*inimigo1, *xInimigo1, obstaculos[1].y, WHITE);
       DrawTexture(*inimigo1, *xInimigo3, obstaculos[3].y, WHITE);
      
   }
   else if (*idxInimigo >= 6 && *idxInimigo <= 11){
       obstaculos[1].x = *xInimigo1 + 30;
       obstaculos[3].x = *xInimigo3 + 30;
       obstaculos[1].width = (*inimigo2).width - 50;
       obstaculos[3].width = (*inimigo2).width - 50;
       obstaculos[1].height = (*inimigo2).height;
       obstaculos[3].height = (*inimigo2).height;
       obstaculos[1].y = 320 - (*inimigo2).height;
       obstaculos[3].y = 320 - (*inimigo2).height;
      
       DrawTexture(*inimigo2, *xInimigo1, obstaculos[1].y, WHITE);
       DrawTexture(*inimigo2, *xInimigo3, obstaculos[3].y, WHITE);
   }
   else if (*idxInimigo >= 12 && *idxInimigo <= 17){
       obstaculos[1].x = *xInimigo1;
       obstaculos[3].x = *xInimigo3;
       obstaculos[1].width = (*inimigo3).width;
       obstaculos[3].width = (*inimigo3).width;
       obstaculos[1].height = (*inimigo3).height;
       obstaculos[3].height = (*inimigo3).height;
       obstaculos[1].y = 320 - (*inimigo3).height;
       obstaculos[3].y = 320 - (*inimigo3).height;
      
       DrawTexture(*inimigo3, *xInimigo1, obstaculos[1].y, WHITE);
       DrawTexture(*inimigo3, *xInimigo3, obstaculos[3].y, WHITE);
   }
   else if (*idxInimigo >= 18 && *idxInimigo <= 23){
       obstaculos[1].x = *xInimigo1;
       obstaculos[3].x = *xInimigo3;
       obstaculos[1].width = (*inimigo4).width;
       obstaculos[3].width = (*inimigo4).width;
       obstaculos[1].height = (*inimigo4).height;
       obstaculos[3].height = (*inimigo4).height;
       obstaculos[1].y = 320 - (*inimigo4).height;
       obstaculos[3].y = 320 - (*inimigo4).height;
      
       DrawTexture(*inimigo4, *xInimigo1, obstaculos[1].y, WHITE);
       DrawTexture(*inimigo4, *xInimigo3, obstaculos[3].y, WHITE);
   }
   *idxInimigo = (*idxInimigo + 1) % 24;
  
}
 
void fecharJogo(Plataforma *flutuantes, Sound *muscamenu, Sound *muscapulo, Sound *muscajogo, Texture2D *textPlacar, Texture2D *texturaMenu, Texture2D *textGameOver, Plataforma *platPrincI, Plataforma *platPrincII, Texture2D *textCenario, Texture2D *textCone, int qtdFlutuantes, Texture2D *move1, Texture2D *move2, Texture2D *move3, Texture2D *move4, Texture2D *move5, Texture2D *move6, Texture2D *move7, Texture2D *inimigo1, Texture2D *inimigo2, Texture2D *inimigo3, Texture2D *inimigo4, Texture2D *jump){
  
  for (int j = 0; j < qtdFlutuantes; j++) UnloadTexture(flutuantes[j].textura);
  free(flutuantes);
 
  UnloadSound(*muscamenu);
  UnloadSound(*muscajogo);
  UnloadSound(*muscapulo);
  UnloadTexture(*texturaMenu);
  UnloadTexture(*textGameOver);
  UnloadTexture(platPrincI->textura);
  UnloadTexture(platPrincII->textura);
  UnloadTexture(*textCenario);
  UnloadTexture(*textCone);
  UnloadTexture(*textPlacar);
  UnloadTexture(*move1);
  UnloadTexture(*move2);
  UnloadTexture(*move3);
  UnloadTexture(*move4);
  UnloadTexture(*move5);
  UnloadTexture(*move6);
  UnloadTexture(*move7);
  UnloadTexture(*jump);
  UnloadTexture(*inimigo1);
  UnloadTexture(*inimigo2);
  UnloadTexture(*inimigo3);
  UnloadTexture(*inimigo4);
 
}


