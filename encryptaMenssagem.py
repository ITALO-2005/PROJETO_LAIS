import rsa
import hashlib
import zipfile
import os

def preparar_envio():
    #verifica se o texto.txt existe antes de iniciar..
    if not os.path.exists("texto.txt"):
        print("Crie um arquivo 'texto.txt' no mesmo diretório antes de rodar.")
        return

    try:
        #Carregar a chave pública gerada pelo Programa 1
        with open("public.pem", "rb") as f:
            pub_key = rsa.PublicKey.load_pkcs1(f.read())

        #Ler o arquivo texto.txt e calcular o SHA-256
        with open("texto.txt", "rb") as f:
            conteudo = f.read()
            
        #O hexdigest é convertido em bytes para poder ser criptografado
        hash_sha256 = hashlib.sha256(conteudo).hexdigest().encode('utf-8')
        
        #Criptografar o hash com a chave pública
        hash_criptografado = rsa.encrypt(hash_sha256, pub_key)

        #saalvar o resultado criptografado
        with open("novotexto.txt", "wb") as f:
            f.write(hash_criptografado)

        #Agrupar texto.txt e novotexto.txt no package.zip
        with zipfile.ZipFile("package.zip", 'w') as zip_ref:
            zip_ref.write("texto.txt")
            zip_ref.write("novotexto.txt")

        print("Processo concluído com sucesso!")
        print("Arquivo 'package.zip' criado com texto.txt e novotexto.txt.")

    except FileNotFoundError as e:
        print(f"Erro de arquivo: certifique-se de ter gerado a chave pública primeiro. ({e})")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

if __name__ == "__main__":
    preparar_envio()