# Sistema visual

## Direção de arte

- Animação 2D educativa, com aparência de ilustração desenhada à mão.
- Contorno grafite `#282828`, espessura visual consistente e formas arredondadas.
- Paleta pastel: cinza azulado, bege, verde suave, coral e azul-marinho.
- Personagens com cabeças expressivas, olhos legíveis e silhuetas simples.
- Cenários cotidianos: escritório, casa, banco, supermercado, cafeteria, cidade e gráficos.
- Composição horizontal 16:9 em 1920×1080.

## Elenco inicial

| ID | Papel | Identidade |
|---|---|---|
| `herbert` | Protagonista | Cabelo branco, camiseta cinza, curioso e acessível. |
| `mentor` | Mentora | Cabelo castanho, óculos, blazer roxo. |
| `investor` | Investidor | Barba curta, cabelo escuro, roupa azul-marinho. |
| `friend` | Amigo | Boné azul, moletom bege, público iniciante. |
| `specialist` | Especialista | Cabelo grisalho, óculos e terno. |

Cada SVG mantém o mesmo `viewBox` e um grupo `#character-rig`. Dez expressões ficam embutidas no SVG e são ativadas pelo motor com `data-expression`.

## Regras de consistência

1. Não altere o formato do rosto nem a escala da cabeça entre expressões.
2. Mantenha o contorno grafite e a paleta definida.
3. Dê preferência a novos assets reutilizáveis em vez de duplicar desenhos dentro de episódios.
4. Novos recursos devem receber IDs curtos em kebab-case e ser registrados em `manifest.json`.
5. Evite texto rasterizado dentro das ilustrações; use a camada de texto do motor para facilitar tradução.
