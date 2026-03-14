# LAB: Utilizando o comando find no Linux

## LAB BÁSICO
### Objetivo
Este laboratório tem como objetivo ensinar a utilizar o comando `find` do Linux para procurar arquivos e diretórios.

### Pré-requisitos
Um ambiente Linux configurado e familiarizado com o terminal.

### Cenário
Você está na sua área de trabalho, que contém vários arquivos e subdiretórios. Você deseja encontrar um arquivo específico sem saber onde ele se encontra.

### Passos
1. Abra o terminal.
2. Utilize o comando `find` para procurar por um arquivo específico. Por exemplo, digite `find / -name meuArquivo.txt`. Isso irá procurar em todo o sistema de arquivos pelo nome do arquivo "meuArquivo.txt".
3. Pressione Enter para executar o comando.
4. O terminal mostrará a localização do seu arquivo, caso ele exista no sistema.

### Desafio extra
Experimente encontrar um diretório vazio na sua área de trabalho digitando `find / -empty`.

### Resultado esperado
Você deve ver a localização do arquivo ou diretório que você procurou no terminal. Se o arquivo não existir, nada será retornado.

## LAB INTERMEDIÁRIO
### Objetivo
Este laboratório tem como objetivo ensinar a utilizar opções adicionais do comando `find` para procurar por tipos de arquivos específicos e localizar arquivos ocultos.

### Pré-requisitos
Conhecimento básico sobre o Linux e familiaridade com o terminal, bem como o laboratório anterior.

### Cenário
Você está trabalhando em um projeto que envolve arquivos de imagem JPEG. Você deseja encontrar todos os arquivos JPEG na sua área de trabalho sem saber onde estão localizados.

### Passos
1. Abra o terminal.
2. Utilize o comando `find` para procurar por arquivos JPEG na sua área de trabalho. Digite `find . -name "*.jpeg"` ou `find . -name "*.jpg"`, dependendo da extensão dos seus arquivos.
3. Pressione Enter para executar o comando.
4. O terminal mostrará a localização de todos os arquivos JPEG na sua área de trabalho.

### Desafio extra
Experimente encontrar arquivos ocultos no seu sistema digitando `find / -name ".*"`.

### Resultado esperado
Você deve ver a localização de todos os arquivos JPEG na sua área de trabalho, além dos arquivos ocultos se existirem.

## LAB AVANÇADO
### Objetivo
Este laboratório tem como objetivo ensinar a utilizar opções mais avançadas do comando `find` para procurar por tamanho de arquivos específicos e localizar arquivos modificados recentemente.

### Pré-requisitos
Conhecimento intermediário sobre o Linux e familiaridade com o terminal, bem como os laboratórios anteriores.

### Cenário
Você está trabalhando em um projeto que envolve arquivos de vídeo grandes. Você deseja encontrar todos os arquivos de vídeo maiores do que 50MB na sua área de trabalho e são modificados recentemente.

### Passos
1. Abra o terminal.
2. Utilize o comando `find` para procurar por arquivos de vídeo grandes mais recentes na sua área de trabalho. Digite `find . -name "*.mp4" -size +50M -mtime -1`.
3. Pressione Enter para executar o comando.
4. O terminal mostrará a localização de todos os arquivos de vídeo maiores do que 50MB na sua área de trabalho e foram modificados recentemente.

### Desafio extra
Experimente encontrar arquivos grandes (mais de 1GB) que não foram acessados nos últimos 2 dias digitando `find / -size +1G ! -atime -2`.

### Resultado esperado
Você deve ver a localização de todos os arquivos de vídeo maiores do que 50MB na sua área de trabalho e foram modificados recentemente, além dos arquivos grandes não acessados nos últimos 2 dias.
