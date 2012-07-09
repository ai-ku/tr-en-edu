import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.Locale;

public class Lowercase {
	public static void main(String[] args) throws IOException {
		BufferedReader input = new BufferedReader(new InputStreamReader(
				System.in, "UTF-8"));
		String line = "";
		
		while ((line = input.readLine()) != null)
			System.out.println(line.toLowerCase(new Locale(args[0])));
		
		if (input != null)
			input.close();
	}
}
