# Memoria-virtual-em-python
Simulador de memória virtual com arquivo para swap de arquivos em python. O programa gera arquivos binário de tamanhos variados entre 60kb e 100kb. 

O programa possui uma classe para as memórias virtuais e para a memória física, cada arquivo possui uma memória virtual que faz o gerenciamento do arquivo quebrando-os em blocos de 4kb e colocando na memória física com um id único para cada arquivo. 

Também é feita a tradução do endereço virtual para o físico usando o offset do bloco. Quando a memória física estiver cheia, o programa seleciona um arquivo aleatório para remover da memória e substituir com um novo. Todos o blocos de 4kb do arquivo removido são escritos em um arquivo binário para representar o swap. 

É possível observar conceitos básicos de como a memória funciona.
