# LAB: mkdir - Criação de diretórios no Linux

## LAB BÁSICO
### Objetivo
Este laboratório tem como objetivo ensinar a criar um único diretório e entender sua sintaxe básica.

### Pré-requisitos
Um ambiente Linux configurado para este laboratório.

### Cenário
Você está na sua máquina local, no terminal do Linux. Você deseja criar um diretório chamado "Projetos".

### Passos
1. Digite o seguinte comando: `mkdir Projetos` e pressione Enter.
2. Verifique se a pasta foi criada digitando `ls` e pressionando Enter. Você deve ver a lista atualizada incluindo "Projetos".

### Desafio extra
Crie um diretório chamado "Documentos" dentro do seu diretório atual.

## LAB INTERMEDIÁRIO
### Objetivo
Neste laboratório, você aprenderá a criar vários diretórios de uma vez e entenderá como usar o parâmetro -p para criar pastas intermediárias automaticamente.

### Pré-requisitos
Você deve ter um ambiente Linux configurado para este laboratório.

### Cenário
Você está na sua máquina local, no terminal do Linux e deseja criar duas pastas chamadas "Pasta1" e "Pasta2".

### Passos
1. Digite o seguinte comando: `mkdir Pasta1 Pasta2` e pressione Enter.
2. Verifique se as pastas foram criadas digitando `ls` e pressionando Enter. Você deve ver a lista atualizada incluindo "Pasta1" e "Pasta2".

### Desafio extra
Crie uma estrutura de diretório com três níveis, como: Pasta1/Pasta2/Pasta3. Use o parâmetro -p para criar automaticamente as pastas intermediárias.

## LAB AVANÇADO
### Objetivo
Neste laboratório avançado, você aprenderá a usar opções comuns do mkdir e entenderá como elas podem ser úteis para cenários de segurança.

### Pré-requisitos
Você deve ter um ambiente Linux configurado para este laboratório.

### Cenário
Você está na sua máquina local, no terminal do Linux e deseja criar uma pasta chamada "Segredo". Você quer definir permissões especiais para essa pasta.

### Passos
1. Digite o seguinte comando: `mkdir -m 755 Segredo` e pressione Enter. O parâmetro "-m" define as permissões da pasta, neste caso, "755", que dá ao proprietário leitura, escrita e execução de permissões, enquanto dá leitura e execução para os membros do grupo e outros.
2. Verifique as permissões da pasta "Segredo" digitando `ls -l` e pressionando Enter. A saída deve mostrar as permissões da pasta "Segredo".

### Desafio extra
Crie uma pasta chamada "ArquivosPrivados", mas dessa vez, use a opção "-Z" para definir um contexto de segurança específico. Por exemplo, você pode usar o contexto "unconfined_u:object_r:user_home_t:s0".

### Resultado esperado
Você terá criado com sucesso pastas no seu sistema Linux e entendido como elas podem ser personalizadas para seus requisitos específicos.