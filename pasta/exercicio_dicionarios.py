"""
 Exercício 3

Dada os dois dicionários abaixo, calcule a média de preços:

```
produtos = [ {
          'produto': 'maça',
          'preco': 2.2
          },
         {
          'produto': 'banana',
          'preco': 1.2
          } ]
everton = {
        'cliente': 'Everton'
        'compra': [ {
                      'produto': 'maça',
                      'qtd' = 3
                     },
                    {
                      'produto': 'banana',
                      'qtd' = 10
                     } ]
}
```
1. Calcule o valor total da compra do Everton
2. Imprima a qtd que ele comprou e o que ele comprou
3. Imprima o valor total das compras
"""
# Calcule o valor total da compra do Everton
# Imprima a qtd que ele comprou e o que ele comprou
# Imprima o valor total das compras

produtos = [{'produto':'maca', 'preco': 2.2},{'produto':'banana', 'preco': 1.1}]
everton = {'cliente': 'everton', 'compra':[{'produto':'maca', 'quantidade':3},{'produto':'banana', 'quantidade':10}]}
qtd = []
for i in produtos:
  qtd.append(i['preco'])
soma = 0
i = 0
for compras in everton['compra']:
  soma += compras['quantidade']*qtd[i]
  i += 1
print(f'A compra de everton deu R$ {soma:.2F}')
for compras in everton['compra']:
  print(f'Everton comprou {compras["quantidade"]} {compras["produto"]}s')
  
  produtos = [{'produto':'maca', 'preco': 2.2},{'produto':'banana', 'preco': 1.1}]
everton = {'cliente': 'everton', 'compra':[{'produto':'maca', 'quantidade':3},{'produto':'banana', 'quantidade':10}]}
soma = 0
i = 0
for compras in everton['compra']:
  soma += compras['quantidade']*produtos[i]['preco']
  i += 1
print(f'A compra de everton deu R$ {soma:.2F}')
for compras in everton['compra']:
  print(f'Everton comprou {compras["quantidade"]} {compras["produto"]}s')
  
  

'''
Dado dicionário abaixo:

    cardapio = {
            'lanche' : 10.9,
            'batata' : 5.5,
            'refri' : 3.9
}
    
1. Mostre o cardápio para o usuário
2. Pergunte quantos itens ele quer de cada
3. Calcule e mostre pra ele o valor total da conta
'''
  
  
  # Declarando dicionário
cardapio = {
            'lanche' : 10.9,
            'batata' : 5.5,
            'refri' : 3.9
}

# 1. Mostrando cardápio:
for k, v in cardapio.items():
  print(f'{k:.<20} R$ {v:5.2f}')

# 2. Perguntando quantos itens ele quer de cada.
qtd = {}
for k in cardapio.keys():
  qtd[k] = int(input(f'Quantos {k} você quer? '))

print(qtd)
# 3. Calculando o valor total:
soma = 0
for v1, v2 in zip(cardapio.values(), qtd.values()):
  soma += v1*v2

# Imprimindo recibo:
print('-'*40)
print('-'*15, 'RECIBO','-'*15)
for k, v in qtd.items():
  print(f'{v} - {k:.<20} = R${v*cardapio[k]:5.2f}')
print(f'O valor total é de R${soma:.2f}')