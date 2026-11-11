# Les 5 Shorts « VALABLE OU PAS ? » suivants (même format que VOP06).  python vop_suite.py VOP01 info|sheet out|frames i n|video
import sys
import pxv, duo
from pxv import Shot, Actor
import serie as S
from serie import acteur, close, duo_shot, board_shot, board, hook, end_shot, polaroid, rows
from textes_suite import T

SK = sys.argv[1]
order, texts = T[SK]
D = S.dialogue(SK, list(order), dict(P=order.count("P"), G=order.count("G")), texts)
L = D.lines
t = lambda k: L[k]["t0"]
te = lambda k: L[k]["t1"] + 0.06
at = D.at
H = S.T_HOOK
W_ = (255, 255, 255); Y_ = (255, 210, 70)


def abl_soeur(t0, t1, **st):
    return Shot(t0, t1, "ablutions", [acteur("S", 482, 1470, mirror=False, **st)],
                cam=(1.45, 1.52, (580, 1150), (590, 1150)))


if SK == "VOP01":
    TITLE = "Du vernis pendant les ablutions"
    shots = [hook([("DU VERNIS ET", W_), ("LES ABLUTIONS ?", Y_)],
                  polaroid("ablutions", (150, 220, 228, 298), "S", pose="mains", face="gene", nails=(220, 40, 60))),
             Shot(H, te(0), "ablutions", [acteur("S", 482, 1470, mirror=False, pose="ablution", face="gene", nails=(220, 40, 60))],
                  cam=(1.45, 1.52, (580, 1150), (590, 1150)), bubbles=[(0, lambda: duo.bulle("?"), 0.1, 9, 10, -2)]),
             board_shot(t(1), te(1), board([(80, "VERNIS = UNE COUCHE", 14, True), (180, "L'EAU NE TOUCHE", 13, False),
                                            (196, "PAS L'ONGLE", 13, False)],
                                           [("main_vernis", 70, 104, 5), ("goutte", 150, 108, 5)])),
             close(t(2), te(2), "P", face="choc", pose="neutre", bubble="?"),
             close(t(3), at(3, "Prophète") - 0.2, "G", pose="explique", face="neutre"),
             board_shot(at(3, "Prophète") - 0.2, te(3), board([(84, "MÊME UNE PARTIE", 14, False), (104, "GRANDE COMME UN ONGLE", 13, True),
                                                               (130, "= ABLUTIONS", 14, False), (150, "À REFAIRE", 14, True)],
                                                              src="SRC  MOUSLIM 243")),
             duo_shot(t(4), te(4), p=dict(pose="question", face="neutre"), g=dict(pose="the", face="neutre")),
             board_shot(t(5), te(5), board([(80, "AVANT CHAQUE ABLUTION :", 12, False), (98, "ON ENLÈVE", 15, True),
                                            (140, "OU : ABLUTIONS D'ABORD,", 12, False), (158, "VERNIS APRÈS", 15, True)],
                                           [("main_vernis", 115, 176, 3)])),
             close(t(6), te(6), "P", face="malin", pose="neutre", bubble="?"),
             end_shot(t(7), D.dur)]

elif SK == "VOP07":
    TITLE = "Un fou rire pendant la priere"
    shots = [hook([("UN FOU RIRE PENDANT", W_), ("LA PRIÈRE ?", Y_)], polaroid("mosquee", who="P", pose="neutre", face="rire")),
             Shot(H, te(0), "mosquee", rows(with_p=Actor("P", 540, 1770, 6, state=lambda u: dict(back=True))),
                  cam=(1.05, 1.16, (540, 1250), (540, 1380)), bubbles=[(12, lambda: duo.bulle("!"), 0.15, 9, 0, -2)]),
             board_shot(t(1), te(1), board([(84, "RIRE AVEC DU BRUIT", 14, True), (104, "+ TU POUVAIS TE RETENIR", 12, False),
                                            (140, "= PRIÈRE ANNULÉE", 15, True), (164, "TU LA RECOMMENCES", 12, False)])),
             close(t(2), te(2), "P", face="gene", pose="question", bubble="?"),
             board_shot(t(3), te(3), board([(84, "CONSENSUS", 15, True), (110, "LE RIRE AVEC DU BRUIT", 12, False),
                                            (128, "ANNULE LA PRIÈRE", 14, False)], src="SRC  IBN QUDAMA, AL-MOUGHNI")),
             close(t(4), te(4), "P", face="choc", pose="panique"),
             close(t(5), te(5), "G", pose="explique", face="neutre"),
             close(t(6), te(6), "P", face="malin", pose="neutre"),
             board_shot(t(7), te(7), board([(90, "LE SOURIRE :", 15, False), (116, "PRIÈRE VALABLE", 15, True),
                                            (146, "(LA PLUPART DES SAVANTS)", 11, False)])),
             close(t(8), te(8), "P", face="rire", pose="pointe", bob=8),
             end_shot(t(9), D.dur)]

elif SK == "VOP04":
    TITLE = "Reveille apres l heure de la priere"
    shots = [hook([("RÉVEILLÉ APRÈS", W_), ("L'HEURE DE PRIÈRE ?", Y_)],
                  polaroid("chambre", (176, 210, 254, 288), "P", pose="panique", face="choc", sweat=True)),
             Shot(H, te(0), "chambre", [acteur("P", 430, 1500, mirror=False, pose="panique", face="choc", sweat=True)],
                  cam=(1.0, 1.06, (560, 1100), (600, 1080)), bubbles=[(0, lambda: duo.bulle("!"), 0.1, 9, 10, -2)]),
             duo_shot(t(1), te(1), p=dict(pose="neutre", face="choc"), g=dict(pose="explique", face="neutre")),
             close(t(2), te(2), "P", face="choc", pose="panique", sweat=True),
             board_shot(t(3), te(3), board([(84, "TU LA PRIES", 15, False), (106, "DÈS TON RÉVEIL", 15, True)],
                                           [("reveil", 105, 132, 5)], src="SRC  MOUSLIM 684")),
             board_shot(t(4), te(4), board([(84, "PAS DE NÉGLIGENCE", 14, True), (106, "DANS LE SOMMEIL", 14, False)],
                                           [("reveil", 105, 132, 5)], src="SRC  MOUSLIM 681")),
             close(t(5), te(5), "P", face="malin", pose="neutre"),
             close(t(6), te(6), "G", pose="explique", face="blase"),
             close(t(7), te(7), "P", face="gene", pose="neutre", bubble="..."),
             Shot(t(8), D.dur, "chambre", [acteur("P", 300, 1500, mirror=False, pose="neutre", face="rire", mute=True, bob=8),
                                           acteur("G", 760, 1500, pose="pointe", face="content")],
                  cam=(1.0, 1.05, (540, 1100), (540, 1080)), overlays=[S.cta_overlay])]

elif SK == "VOP08":
    TITLE = "Prier avec un tatouage"
    shots = [hook([("UN TATOUAGE :", W_), ("PRIÈRE VALABLE ?", Y_)], polaroid("salon", (110, 200, 188, 278), "P", pose="question", face="neutre")),
             duo_shot(H, te(0), p=dict(pose="question", face="neutre"), g=dict(pose="the", face="neutre")),
             board_shot(t(1), te(1), board([(80, "PRIÈRE VALABLE", 15, True), (100, "(LA PLUPART DES SAVANTS)", 11, False),
                                            (176, "L'ENCRE EST SOUS LA PEAU", 12, False)],
                                           [("bras_tatoue", 70, 120, 5), ("goutte", 160, 118, 4)])),
             close(t(2), te(2), "P", face="malin", pose="neutre"),
             close(t(3), at(3, "Prophète") - 0.2, "G", pose="explique", face="choc"),
             board_shot(at(3, "Prophète") - 0.2, te(3), board([(90, "LE TATOUAGE", 15, False), (112, "EST INTERDIT", 15, True),
                                                               (140, "(HOMMES ET FEMMES)", 11, False)], src="SRC  BOUKHARI 5937")),
             close(t(4), te(4), "P", face="gene", pose="neutre", bubble="?"),
             board_shot(t(5), te(5), board([(80, "1. IL SE REPENT", 14, True), (112, "2. L'ENLEVER SI POSSIBLE", 12, False),
                                            (128, "SANS DANGER", 12, False), (146, "(CHAFÉITES ET D'AUTRES)", 11, False)])),
             close(t(6), te(6), "P", face="content", pose="pointe"),
             end_shot(t(7), D.dur)]

elif SK == "VOP09":
    TITLE = "Faux ongles henne maquillage"
    shots = [hook([("FAUX ONGLES, HENNÉ,", W_), ("MAQUILLAGE ?", Y_)],
                  polaroid("ablutions", (150, 220, 228, 298), "S", pose="mains", face="gene", nails=(240, 120, 170))),
             abl_soeur(H, te(0), pose="mains", face="gene", nails=(240, 120, 170)),
             board_shot(t(1), te(1), board([(84, "L'EAU DOIT TOUCHER", 14, False), (104, "LA PEAU ET L'ONGLE", 14, True)],
                                           [("goutte", 115, 130, 5)], src="SRC  MOUSLIM 243")),
             close(t(2), te(2), "P", face="neutre", pose="question", bubble="?"),
             board_shot(t(3), te(3), board([(84, "FAUX ONGLES", 15, False), (106, "PAS VALABLE", 15, True),
                                            (196, "ON LES ENLÈVE AVANT", 12, False)], [("faux_ongle", 105, 128, 5)])),
             close(t(4), te(4), "P", face="neutre", pose="question", bubble="?"),
             board_shot(t(5), te(5), board([(84, "HENNÉ", 15, False), (106, "VALABLE", 15, True),
                                            (196, "ENLÈVE BIEN LA PÂTE", 12, False)], [("main_henne", 105, 128, 5)],
                                           src="SRC  AN-NAWAWI, AL-MAJMOU'")),
             close(t(6), te(6), "P", face="neutre", pose="question", bubble="?"),
             board_shot(t(7), te(7), board([(78, "COUCHE (WATERPROOF) :", 12, False), (94, "ON ENLÈVE", 14, True),
                                            (184, "COULEUR (KHÔL) : ÇA PASSE", 11, False)],
                                           [("mascara", 70, 116, 5), ("khol", 150, 116, 5)], src="SRC  COMITÉ PERMANENT DES FATWAS")),
             close(t(8), te(8), "P", face="malin", pose="neutre", bubble="..."),
             end_shot(t(9), D.dur)]

VID = pxv.Video(D, shots, music=S.MUSIC, music_gain=0.10)
sys.argv = [sys.argv[0]] + sys.argv[2:]
S.main(VID, D, SK, TITLE)
