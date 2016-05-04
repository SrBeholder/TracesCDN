package coletor;
 
import java.io.*;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import org.apache.http.HttpResponse;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.impl.client.HttpClientBuilder;
 
public class Coletor {
    
    //Método de carregar página e obter informação desejada
    public void getPage(String url, File file, String time) throws IOException {
        //Parâmetros para abertura do endereço
        final String USER_AGENT = "Google Chrome.Ink";
	HttpClient client = HttpClientBuilder.create().build();
	HttpGet request = new HttpGet(url);
	request.addHeader("User-Agent", USER_AGENT);
	HttpResponse response = client.execute(request);
        
        //Definição de Buffers: Entrada (página carregada) e Saída (arquivo criado e passado como parâmetro)
        BufferedReader in = new BufferedReader(new InputStreamReader(response.getEntity().getContent()));
        BufferedWriter out = new BufferedWriter(new FileWriter(file));
        String inputLine;
        
        //Escreve a hora que o arquivo foi gerado e pula linha
        out.write(time);
        out.newLine();
        
        //Varre todas as linhas da página procurando a tag meta com informação da data de publicação
        //Quando encontra o programa encreve no arquivo
        while ((inputLine = in.readLine()) != null) {    
            Matcher regex = Pattern.compile("(?<=datePublished\" content=\")(.*)(?=\" />)").matcher(inputLine);
            if(regex.find()){
                out.write(regex.group(1));
                out.newLine();
            }  
        }

        //Fecha o arquivo de leitura e finaliza arquivo usado para escrever as saídas
        in.close();
        out.flush();
        out.close();
    }
 
    //Método principal do programa
    public static void main(String[] args) throws IOException {

        System.out.println("Executando com sucesso");

        //Cria variáveis de tempo
        long tempoAtual = System.currentTimeMillis();
        String time = "" + System.currentTimeMillis();

        //Cria arquivo no disco
        File file = new File("arquivo.txt");
              
        //Chama função de carregar a página
        new Coletor().getPage("http://gshow.globo.com/novelas/totalmente-demais/capitulo/2015/11/30/eliza-diz-arthur-que-desistiu-do-concurso.html", file, time);
    }
}