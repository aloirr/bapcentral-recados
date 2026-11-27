# Visitas da Máxima no site: o que o Alexandre faz (T-0045)

São 9 passos. Os passos 1 e 2 podem ser feitos já. Os passos 3 a 9 só depois que o time avisar que o código está no ar.

**Na Máxima**

1. **Crie um usuário só para o robô.** Use um nome que diga para que ele serve, por exemplo "robô de visitas BAP". Use um e-mail da empresa que não seja de uma pessoa, se a Máxima pedir um.
2. **Dê a esse usuário só o mínimo:** acesso ao maxGestão, somente leitura, só no Painel Auditoria (Espelho de Rotas), com todas as filiais, supervisores e representantes. Sem cadastro, sem pedido e sem administração. Guarde o usuário e a senha só com você: não mande ao time, nem por recado nem por mensagem.

**No Render (depois do aviso do time)**

3. **Dê o "autorizo" que o po vai pedir** para o PR do `render.yaml`. Ele já vem com o número e o código do commit.
4. **Depois do merge, abra o painel do Render** e veja se o serviço novo **bap-visitas-maxima** apareceu, junto do **bap-central**. Se o site foi criado pelo Blueprint, ele aparece sozinho em alguns minutos (o Render pode pedir que você confirme o sync do Blueprint). Se não aparecer, avise o po: o time manda o jeito de criar à mão.
5. **Abra o bap-visitas-maxima > Environment.** Preencha só as duas variáveis vazias:
   - `BAP_MAXIMA_USUARIO`: o usuário do passo 1;
   - `BAP_MAXIMA_SENHA`: a senha dele.
   Salve. As outras variáveis já vêm prontas, e o `BAP_VISITAS_TOKEN` o próprio Render cria. Não mexa nelas.
6. **Confira o plano e o preço:** no bap-visitas-maxima > Settings, o plano deve ser o de 2 GB (Standard), cobrado por minuto. Se o preço estiver muito diferente de US$ 1 a 3 por mês, avise o po antes de seguir.

**O primeiro teste (diagnóstico)**

7. **Espere até 10 minutos, ou clique em "Trigger Run"** no bap-visitas-maxima para rodar na hora. Essa primeira rodada é só um teste: entra na Máxima, abre um dia com dois vendedores e mede memória e tempo. Ela não grava visita nenhuma.
8. **Veja o resultado em bap-visitas-maxima > Logs.** Procure a linha que começa com `DIAGNOSTICO`:
   - `codigo=OK`: deu certo. Mande ao po "diagnóstico ok";
   - `MAXIMA_CONFIRMACAO`, `MAXIMA_CAPTCHA` ou `MAXIMA_BLOQUEIO`: a Máxima pediu confirmação ou barrou o acesso vindo do Render. Nada é tentado de novo. Mande o código ao po, e o time traz as saídas;
   - `MAXIMA_SENHA`: corrija a senha no passo 5 e, no site, clique em "Retomar";
   - qualquer outro código: mande só o código ao po.
   O log nunca mostra senha, usuário nem nome de vendedor. O mesmo resultado aparece no site, em Farol de Visita > Atualizar visitas, para o admin.

**Ligar a rotina**

9. **Com o "diagnóstico ok", entre no site como admin** e, em Farol de Visita > Atualizar visitas, clique em **"Ligar a agenda"**. A partir daí, o site baixa ontem todo dia às 06h00, e admin e gerente podem apertar "Atualizar visitas" (até 7 dias). O botão do PC continua funcionando como hoje.

**Se um dia precisar trocar a senha da Máxima:** troque só no passo 5 e clique em "Retomar" no site. **Para desligar tudo:** clique em "Desligar a agenda" no site, ou suspenda o bap-visitas-maxima no Render (Settings > Suspend).
