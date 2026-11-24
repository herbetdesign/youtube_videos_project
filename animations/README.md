# Presets de animação

Os movimentos básicos são aplicados pelo `engine/engine.js` com base no campo `movement` de cada cena. IDs iniciais: `idle`, `talking`, `typing`, `thinking`, `walking`, `pointing`, `celebrating`, `holding_phone`, `holding_money`, `writing`.

Câmeras: `static`, `slow_zoom_in`, `slow_zoom_out`, `pan_left`, `pan_right`.

Ao adicionar um movimento real, implemente-o no método `movementTransform()` e registre o ID no `manifest.json`. O preset atual usa deslocamentos leves de rig; movimentos específicos de braços/mãos serão uma evolução futura.
