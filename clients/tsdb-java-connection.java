package pg;

import java.sql.Connection;
import java.sql.DriverManager;
import java.util.Properties;

public final class Connect {
  public static void main(String[] args) {
    Properties props = new Properties();
    props.put("jdbc.url", "jdbc:postgresql://YOUR-SERVICE.a.timescaledb.io:20985/defaultdb");
    props.put("user", "YOUR-USER");
    props.put("password", "YOUR-PASSWORD");
    props.put("ssl", "true");
    props.put("sslmode", "verify-ca");
    props.put("sslrootcert", "/path/to/ca.pem");

    try {
      Connection c = DriverManager.getConnection(props.getProperty("jdbc.url"), props);
      System.out.println("Success");
      c.close();
    } catch (Exception e) {
      e.printStackTrace();
    }
  }
}
