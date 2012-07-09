import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.Locale;

public class ParseHasimOutput {
	public static void main(String[] args) throws IOException {
		BufferedReader input = new BufferedReader(new InputStreamReader(
				new FileInputStream(args[0])));
		String line = "";
		
		while ((line = input.readLine()) != null) {
			if (line.startsWith("<S>") || line.startsWith("</S>"))
				System.out.println(line.split(" ")[0]);
			else {
				if (line.equals("") || line.trim().equals(""))
					continue;
				if (!line.contains(" ")) {
					System.out.println(line);
					continue;
				}
				if (line.split(" ").length == 1) {
					System.out.println(line);
					continue;
				}
				
				String s = line.split(" ")[1];
				s = s.toLowerCase(new Locale("tr"));
				
				if (s.equals("") || s.equals(" ")) {
					System.out.println(line.split(" ")[0]);
					continue;
				}
				
				if (s.length() > 1 && (s.contains("+") || s.contains("-"))) {
					s = s.replace("-", "+");
					s = s.replace("+", " +");
				}
				
				s = s.trim();
				
				if (!s.equals(""))
					System.out.println(s);
			}
		}
		
		input.close();
	}
}
