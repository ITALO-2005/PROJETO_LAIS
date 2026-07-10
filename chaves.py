import rsa
import zipfile
import hashlib
import os
def menu():
    while True:
        print("\n--- Sistema de Gerenciamento ---")
        print("1. Gerar chaves RSA (1024 bits)")
        print("2. Descompactar pacote (package.zip)")
        print("3. Validar Autenticidade do Arquivo")
        print("4. Sair")
        
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            print("Gerando chaves, aguarde...")
            pub_key, priv_key = rsa.newkeys(1024)
            
            with open("public.pem", "wb") as f:
                f.write(pub_key.save_pkcs1())
            with open("private.pem", "wb") as f:
                f.write(priv_key.save_pkcs1())
                
            print("Chaves public.pem e private.pem geradas com sucesso!")

        elif opcao == '2':
            if not os.path.exists("package.zip"):
                print("Erro: Arquivo 'package.zip' não encontrado.")
                continue
            
            if not os.path.exists("extracted"):
                os.makedirs("extracted")
                
            with zipfile.ZipFile("package.zip", 'r') as zip_ref:
                zip_ref.extractall("extracted")
            print("Pacote descompactado com sucesso na pasta 'extracted'.")

        elif opcao == '3':
            try:
                # Carregar a chave privada para decifrar
                with open("private.pem", "rb") as f:
                    priv_key = rsa.PrivateKey.load_pkcs1(f.read())

                # Ler o texto extraído e calcular o hash SHA-256 atual
                with open("extracted/texto.txt", "rb") as f:
                    conteudo_texto = f.read()
                hash_atual = hashlib.sha256(conteudo_texto).hexdigest().encode('utf-8')

                #ler o hash criptografado enviado
                with open("extracted/novotexto.txt", "rb") as f:
                    hash_criptografado = f.read()

                # Descriptografar o hash original
                hash_original = rsa.decrypt(hash_criptografado, priv_key)

                # Comparação
                if hash_atual == hash_original:
                    print("\n>>> Arquivo Autêntico <<<")
                else:
                    print("\n>>> Arquivo não Autêntico <<<")
                    
            except FileNotFoundError:
                print("Erro: Os arquivos necessários não foram encontrados. Execute a extração primeiro.")
            except rsa.pkcs1.DecryptionError:
                print("\n>>> Arquivo não Autêntico <<< (Falha na descriptografia)")
            except Exception as e:
                print(f"Erro inesperado: {e}")

        elif opcao == '4':
            print("encerrando..")
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    menu()