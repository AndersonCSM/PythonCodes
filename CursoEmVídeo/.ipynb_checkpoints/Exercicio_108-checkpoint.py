# Exercicio_108
from utilidades import moeda

valor = float(input('Digite um valor em R$. \n'))

print(f'A metade de {moeda.moeda(valor)} é {moeda.moeda(moeda.metade(valor))}')
print(f'O dobro de {moeda.moeda(valor)} é {moeda.moeda(moeda.dobro(valor))}')
print(f'Aumentando 10% de {moeda.moeda(valor)} temos {moeda.moeda(moeda.aumentar(valor,10))}')
print(f'Diminuindo 13% de {moeda.moeda(valor)} temos {moeda.moeda(moeda.diminuir(valor,13))}')
