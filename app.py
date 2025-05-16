import cv2
import dash_mantine_components as dmc
import plotly.express as px
import plotly.graph_objects as go
import random

from dash import Dash, html, dcc, callback, Output, Input
app = Dash(__name__)
server = app.server

#dictionnaire des photots
dico_image = {"zvb.jpg": [(161, 181), (174, 187)],
              "yth.jpg": [(156, 245), (215, 282)],
              "xwd.jpg": [(277, 66), (315, 89)],
              "xsw.jpg": [(229, 221), (292, 255)],
              "xdd.jpg": [(309, 61), (344, 89)],
              "wdf.jpg": [(37, 276), (129, 327)],
              "wcw.jpg": [(160, 42), (193, 61)],
              "vsw.jpg": [(181, 223), (228, 252)],
              "vsq.jpg": [(148, 177), (186, 198)],
              "uil.png": [(145, 314), (191, 344)],
              "ugj.jpg": [(208, 178), (313, 211)],
              "tyh.jpg": [(160, 132), (186, 152)],
              "trd.jpg": [(239, 129), (289, 153)],
              "sqz.jpg": [(227, 89), (241, 95)],
              "sdx.png": [(287, 273), (300, 279)],
              "rty.jpg": [(274, 75), (305, 96)],
              "rez.jpg": [(176, 59), (210, 78)],
              "res.jpg": [(97, 127), (120, 143)],
              "qwv.jpg": [(76, 153), (97, 168)],
              "qqd.jpg": [(82, 83), (100, 94)],
              "qje.jpg": [(261, 102), (274, 109)],
              "pty.png": [(200, 73), (224, 88)],
              "poi.png": [(273, 217), (315, 230)],
              "pil.jpg": [(174, 208), (217, 228)],
              "pfg.jpg": [(175, 112), (234, 139)],
              "nbg.jpg": [(219, 318), (255, 343)],
              "lhf.jpg": [(69, 135), (76, 138)],
              "kgw.jpg": [(113, 263), (122, 268)],
              "jhg.png": [(84, 76), (97, 92)],
              "ium.jpg": [(190, 229), (228, 260)],
              "irn.jpg": [(186, 129), (201, 139)],
              "igp.jpg": [(34, 141), (46, 149)],
              "glo.png": [(170, 227), (191, 240)],
              "fsz.png": [(205, 192), (243, 208)],
              "ezv.jpg": [(199, 156), (207, 163)],
              "ert.png": [(57, 152), (66, 156)],
              "cwq.png": [(219, 130), (247, 155)],
              "css.jpg": [(271, 131), (291, 145)],
              "cqx.jpg": [(256, 272), (297, 289)],
              "cri.png": [(177, 53), (181, 58)],
              "cds.jpg": [(232, 141), (246, 150)],
              "cas.jpg": [(39, 153), (45, 161)],
              "bni.jpg": [(99, 234), (121, 247)],
              "bcd.jpg": [(287, 150), (299, 166)],
              "azs.jpg": [(275, 240), (283, 245)],
              "axw.png": [(44, 121), (49, 125)],
              "aaj.jpg": [(315, 326), (324, 332)]}

#fonction pour afficher la photo
def show_photo(nom_photo="zzz.jpg", x=0, y=0, show_square=False):
    im = cv2.imread(f"./photos/{nom_photo}")
    #afficher zones cliquables
    if show_square:
        for i in dico_image.values():
            color = (random.randrange(0,255),  random.randrange(0,255),  random.randrange(0,255))
            thickness = 2
            im = cv2.rectangle(im, i[0], i[1], color, thickness)
    im = im[:, :, [2, 1, 0]]

    #aficher la photo
    fig = px.imshow(im)
    fig.update_xaxes(visible=False, showticklabels=False, showgrid=False, showline=False)
    fig.update_yaxes(visible=False, showticklabels=False, showgrid=False, showline=False)
    fig.update_layout(plot_bgcolor="rgba(0, 0, 0, 0)", margin=dict(l=0, r=0, t=0, b=0), autosize=True)
    fig.update_traces(hovertemplate="<extra></extra>")


    if nom_photo != "zzz.jpg":
        fig.add_trace(go.Scatter(x=[x], y=[y], mode="markers", marker=dict(size=15, color="red")))

    return fig

#fonction pour récupérer le clique
def clique_to_nose(x, y):
    lst_img = []
    for k in dico_image.keys():
        condition1 = dico_image[k][0][0] <= x <= dico_image[k][1][0]
        condition2 = dico_image[k][0][1] <= y <= dico_image[k][1][1]
        if (condition1 and condition2):
            lst_img.append(k)
    
    if len(lst_img) >= 1:
        img_name = random.choice(lst_img)
    else:
        img_name = "qpl.png"
    return img_name
  
#corps de l'application
app.layout = dmc.MantineProvider(
    forceColorScheme="light",
    children=[html.Div([
        html.Center(dcc.Graph(figure=show_photo(), id="final-figure")),
        html.Br(),
        dmc.Text(dmc.Center(dmc.Text("Cliquez où vous le souhaitez", size="xl"))),
        dmc.Text(dmc.Center(dmc.Text("Mon nez s'affichera à l'endroit de votre clic", size="xl"))),
        html.Br(),
        dmc.Center(dmc.Switch(id="switch", size="lg", radius="lg", label="Afficher les zones cliquables",checked=False))])])

#callback pour changer image en fonction du clique
@callback(Output(component_id="final-figure", component_property="figure"),
          [Input("final-figure", "clickData"), Input("switch", "checked")],
          prevent_initial_call=True)
def update_image(clickdata, switch):
    #afficher solution
    solution = True if switch else False
    
    #si pas de clique
    if clickdata is None:
        return show_photo(show_square=solution)

    #récuperer les coordonnées
    x = clickdata['points'][0]['x']
    y = clickdata['points'][0]['y']
    img_name = clique_to_nose(x, y)

    # Afficher l'image associée
    return show_photo(img_name, x, y, solution)



if __name__ == "__main__":
    app.run(debug=True)
