import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.Arrays;
import java.util.HashSet;

public class ParseTreeTaggerOutput {
	
	//english tag list used in (oflazer, 2009)
	static String[] tagList = { "NNS", "VV", "VB", "VH", "VVD", "VBD", "VHD",
			"VVG", "VBG", "VHG", "VVN", "VBN", "VHN", "VVZ", "VBZ", "VHZ",
			"VVP", "VBP", "VHP" };
	
	public static void main(String[] args) throws IOException {
		HashSet<String> tags = new HashSet<String>(Arrays.asList(tagList));
		
		BufferedReader input = new BufferedReader(new InputStreamReader(
				new FileInputStream(args[0])));
		String line = "";
		
		while ((line = input.readLine()) != null) {
			if (line.equals("<S>") || line.equals("</S>"))
				System.out.println(line);
			else {
				if(!line.contains("\t")){
					System.out.println(line);
					continue;
				}
				
				String surface = line.split("\t")[0];
				String tag = line.split("\t")[1];
				String lemma = line.split("\t")[2];
				
				if (tags.contains(tag))
					System.out.println(lemma + " +" + tag.toLowerCase());
				else
					System.out.println(surface);
			}
			
		}
		
		input.close();
	}
}
