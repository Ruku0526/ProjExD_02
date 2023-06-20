import random
import sys
import pygame as pg


WIDTH, HEIGHT = 1600, 900

delta ={
    pg.K_UP: (0,-5),
    pg.K_DOWN: (0,+5),
    pg.K_LEFT: (-5,0),
    pg.K_RIGHT: (+5,0),
}

bd_imgs = []

def check_bound(rect: pg.Rect) -> tuple[bool, bool]:
    """
    こうかとんRectや爆弾Rectが画面外 or 画面内かを判定する関数
    引数： こうかとんRect or 爆弾Rect
    戻り値：横方向 縦方向の判定結果タプル （True:画面内 False: 画面外）
    """
    yoko, tate = True, True
    if rect.left < 0 or WIDTH < rect.right: #横方向判定
        yoko = False
    if rect.top < 0 or HEIGHT < rect.bottom: #縦方向判定
        tate = False
    return yoko, tate
def  roto(sum):
    kk_img_o = pg.image.load("ex02/fig/3.png")
    kk_img = pg.transform.flip(kk_img_o,True,False)
    img1 = pg.transform.rotozoom(kk_img_o, 0, 2.0) 
    img2 = pg.transform.rotozoom(kk_img_o, 45, 2.0)
    img3 = pg.transform.rotozoom(kk_img_o, -45, 2.0)
    img4 = pg.transform.rotozoom(kk_img_o, 90, 2.0)
    img5 = pg.transform.rotozoom(kk_img, 90, 2.0)
    img6 = pg.transform.rotozoom(kk_img, 0, 2.0)
    img7 = pg.transform.rotozoom(kk_img, 45, 2.0)
    img8 = pg.transform.rotozoom(kk_img, -45, 2.0)

    imgs = {
        (0,0):img1,
        (0,5):img4,
        (0,-5):img5,
        (5,5):img8,
        (5,-5):img7,
        (-5,5):img2,
        (-5,-5):img3,
        (-5,0):img1,
        (5,0):img6


    }
    return imgs[tuple(sum)]
def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("ex02/fig/pg_bg.jpg")
    kk_img = pg.image.load("ex02/fig/3.png")
    kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)
    kk_rct = kk_img.get_rect()
    bd_img = pg.Surface((20,20))
    pg.draw.circle(bd_img,(255,0,0),(10,10),10)
    bd_imgs.append(bd_img)
    bd_img.set_colorkey((0,0,0))
    x = random.randint(0,WIDTH)
    y = random.randint(0,HEIGHT)
    clock = pg.time.Clock()
            #爆弾Surfaceから爆弾Rectを抽出する
    bd_rct = bd_img.get_rect() 
    bd_rct.center = x,y #爆弾Rectの中心座標を乱数で指定する
    vx, vy = +5,+5
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bd_rct):
            print("game over")
            return 
        key_lst=pg.key.get_pressed()
        sum_mv = [0,0]
        for k, mv in delta.items():
            if key_lst[k]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        kk_rct.move_ip(sum_mv[0], sum_mv[1])
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0],-sum_mv[1])
        kk_img = roto(sum_mv)
        accs = [a for a in range(1,11)]
        avx,avy = vx*accs[min(tmr//500,9)], vy*accs[min(tmr//500,9)]
        screen.blit(bg_img, [0, 0])
        screen.blit(kk_img, kk_rct)
        screen.blit(bd_img, bd_rct)
        bd_rct.move_ip(avx,avy)
        yoko, tate = check_bound(bd_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()