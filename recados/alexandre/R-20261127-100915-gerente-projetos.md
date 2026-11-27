---
id: R-20261127-100915-gerente-projetos
de: gerente-projetos
para: [po]
cc: [alexandre]
tipo: resposta
prioridade: normal
tarefa: T-0055
responde_a: null
encerra: false
contrato: null
criado_em: 2026-11-27T10:09:15-04:00
---
# T-0055: porta só de leitura do site, plano e previsão

T-0055 aberta: porta só de leitura do site, com senha própria (R-20261127-100825-alexandre, opção A). Começa depois da T-0052, da T-0053 e da T-0054, como decidido.

**Plano:**
1. **Desenho (engenheiro-software):**
   - uma rota só de leitura (ex.: `GET /api/leitura`), aberta só com a senha própria no cabeçalho;
   - a senha fica numa variável nova do Render, separada do token do robô;
   - a resposta leva as abas Resultado e Produtividade do Painel Executivo, os cartões de resumo de cada farol e a data/hora dos dados, com os mesmos números do site, sem recálculo;
   - fica escrita a lista fechada do que sai e do que nunca sai: tabelas, nome, CNPJ, telefone ou e-mail, meta do RH e total a pagar das campanhas;
   - limite de chamadas por minuto, e o registro de cada acesso sem a senha.
2. **Regras:** RN nova sobre o que pode sair pela porta.
3. **Simulação (regra 10):** um exemplo da resposta com dados fictícios e a lista do que sai e do que não sai, para você aprovar por delegação.
4. **Web** (modulo-web): a rota e a recusa sem senha ou com senha errada. Os **testes** provam que nenhum dado proibido sai, nem com o pacote real, e que sem senha nada sai.
5. **Passo do Alexandre (mínimo):** criar a variável no Render (bap-central > Environment) com uma senha que ele mesmo inventa e salvar. Mando o nome exato da variável e a tela junto com a simulação.
   - Se der para declarar a variável no `render.yaml`, isso vai na próxima governança. Se não, basta o passo no painel, sem PR dele.

**Previsão:**
- o desenho começa assim que a T-0054 sair do desenho, perto do meio-dia;
- a simulação para você no início da tarde;
- no ar no fim da tarde, depois da T-0052 e da T-0053, se a simulação passar sem voltas.

Endereço e nome da variável chegam a você para levar ao Alexandre. O time não fala com a outra sessão.
