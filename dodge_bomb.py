import random
import sys
import pygame as pg


WIDTH, HEIGHT = 1600, 900
delta = {  # 練習3
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0)
}


def check_bound(rct: pg.Rect) -> tuple[bool, bool]:  # 練習4
    """
    オブジェクトが画面内or画面買いを判定し、真理値タプルを返す関数
    引数 rct：こうかとんor爆弾SurfaceのRect
    戻り値：横方向、縦方向はみだし判定結果（画面内：True/画面外：False）
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False
    return yoko, tate


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("ex02/fig/pg_bg.jpg")
    kk_img = pg.image.load("ex02/fig/3.png")
    kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)
    kk_rct = kk_img.get_rect()  # 練習3 
    kk_rct.center = 900, 400  # 練習3
    bb_img = pg.Surface((20, 20))   # 練習1　透明の四角（surface）
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)  # 練習1
    bb_img.set_colorkey((0, 0, 0))  # 練習1
    bb_rct = bb_img.get_rect()  # 練習1
    bb_rct.centerx = random.randint(0, WIDTH)  # 練習1
    bb_rct.centery = random.randint(0, HEIGHT)  # 練習1
    vx, vy = +5, +5  # 練習2

    kk_muki = {  # 課題1　画像表示する辞書の作成
            (0, 0)  :pg.transform.rotozoom(kk_img, 0, 1.0),
            (-5, 0) :pg.transform.rotozoom(kk_img, 0, 1.0),
            (0, -5) :pg.transform.rotozoom(kk_img, 270, 1.0),
            (+5, -5):pg.transform.rotozoom(pg.transform.flip(kk_img, True, False), 45, 1.0),
            (+5, 0) :pg.transform.rotozoom(pg.transform.flip(kk_img, True, False), 0, 1.0),
            (+5, +5):pg.transform.rotozoom(pg.transform.flip(kk_img, True, False), 315, 1.0),
            (0, +5) :pg.transform.rotozoom(kk_img, 90, 1.0),
            (-5, +5):pg.transform.rotozoom(kk_img, 45, 1.0),
            (-5, -5):pg.transform.rotozoom(kk_img, 315, 1.0),
            }

    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
            
        if kk_rct.colliderect(bb_rct):  
            last_coordinate = kk_rct.center  # 課題3 爆弾に当たった座標を保存
            kk_img = pg.image.load("ex02/fig/8.png")  # 課題3 画像読み込み
            kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)
            kk_rct = kk_img.get_rect() 
            kk_rct.center = last_coordinate  # 課題3 爆弾に当たった座標に表示
            screen.blit(kk_img, kk_rct)  # 課題3 画像を表示
            pg.display.update()
            clock.tick(1.0)  # 課題3 時間の進みを遅くし表示時間を伸ばす
            print("Game Over")
            return
        
        key_lst = pg.key.get_pressed()  # 練習3
        sum_mv = [0, 0]
        for k, tpl in delta.items():
            if key_lst[k]:
                sum_mv[0] += tpl[0]
                sum_mv[1] += tpl[1]
                kk_img = kk_muki[tuple(sum_mv)]  # 課題1　入力方向に沿った向きの画像を表示

        screen.blit(bg_img, [0, 0])
        kk_rct.move_ip(sum_mv[0], sum_mv[1])  #練習3
        screen.blit(kk_img, kk_rct)  # 練習3
        if check_bound(kk_rct) != (True, True):  #練習4
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        bb_rct.move_ip(vx, vy)  # 練習2
        yoko, tate = check_bound(bb_rct)  #練習4
        if not yoko:  #練習4
            vx *= -1
        if not tate:
            vy *= -1

        screen.blit(bb_img, bb_rct)  # 練習1
        pg.display.update()
        tmr += 1
        clock.tick(100)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()