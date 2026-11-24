# Prompt para roteiro e storyboard no ChatGPT

Use o seguinte pedido como ponto de partida:

> Crie um roteiro para um vídeo de YouTube sobre **[TEMA]**, com duração aproximada de **[DURAÇÃO]**. Entregue roteiro de narração e storyboard cena a cena para o Financial Animation Kit. Mantenha estilo 2D cartoon pastel, contorno grafite e formato 16:9. Use somente os personagens, cenários, objetos, expressões, movimentos e câmeras listados no `manifest.json` fornecido. Não invente IDs. Para cada cena, informe: ID, duração, cenário, personagem, expressão, movimento, coordenada aproximada do personagem (x/y entre 0 e 1), objetos com coordenadas e dimensões, movimento de câmera, texto na tela e narração. Varie enquadramentos e cenas; evite trocar de fundo sem motivo narrativo. Depois, entregue também o JSON de episódio seguindo `data/episode.schema.json`.

Para economizar tokens, forneça ao ChatGPT apenas o `manifest.json`, o schema e a descrição do episódio. Não é necessário enviar o conteúdo integral de cada SVG, a menos que seja solicitado um ajuste visual daquele asset.
