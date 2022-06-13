package com.example.getapi;

import static java.lang.Thread.sleep;

import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.NotificationCompat;
import androidx.core.app.NotificationManagerCompat;

import android.app.Notification;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.os.Build;
import android.os.Bundle;
import android.util.Log;
import android.widget.ProgressBar;
import android.widget.TextView;


import com.example.getapi.databinding.ActivityMainBinding;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.Calendar;
import java.util.Date;
public class MainActivity extends AppCompatActivity {

    ActivityMainBinding binding;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        binding = ActivityMainBinding.inflate(getLayoutInflater());
        setContentView(binding.getRoot());
        new fetchData().start();

    }
    public static String removeFirstandLast(String str)
    {
        str = str.substring(1, str.length() - 1);
        return str;
    }
    public int iD_no=1;
    class fetchData extends Thread{

        @Override
        public void run() {
            createNotificationChannel();
            while (true){
            String data="";


                try {
                    URL url = new URL("https://lab3-iot-nodejs.herokuapp.com/v1/data");
                    HttpURLConnection httpURLConnection = (HttpURLConnection) url.openConnection();
                    InputStream inputStreamReader = httpURLConnection.getInputStream();
                    BufferedReader bufferedReader = new BufferedReader(new InputStreamReader(inputStreamReader));
                    String line = "";
                    while ((line = bufferedReader.readLine()) != null) {
                        data = data + line;
                    }
                    data = removeFirstandLast(data);
                    JSONObject jsonObject = new JSONObject(data);
                    String a = jsonObject.getString("temperature");
                    String b = jsonObject.getString("humidity");
                    String c = jsonObject.getString("detect");
                    if (c.equals("1")){
                        new CreateNotify().start();
                    }
                    runOnUiThread(new Runnable() {
                        @Override
                        public void run() {
                            //Do something here to change UI
                            TextView tv1 = (TextView) findViewById(R.id.humidityTextView);
                            TextView tv2 = (TextView) findViewById(R.id.humidityTextView1);
                            ProgressBar pg1 = (ProgressBar) findViewById(R.id.humidityProgressBar);
                            ProgressBar pg2 = (ProgressBar) findViewById(R.id.humidityProgressBar1);
                            tv1.setText(b + "%");
                            tv2.setText(a + "°C");
                            pg1.setProgress(Integer.parseInt(b));
                            pg2.setProgress(Integer.parseInt(a));
                        }
                    });
                    //String a = jsonObject.getString("detect");
                } catch (MalformedURLException e) {
                    e.printStackTrace();
                } catch (IOException e) {
                    e.printStackTrace();
                } catch (JSONException e) {
                    e.printStackTrace();
                }
                try {
                    sleep(5000);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
            }

        }
    private void createNotificationChannel() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            CharSequence name = "Channel";
            String description = "This is channel";
            int importance = NotificationManager.IMPORTANCE_DEFAULT;
            NotificationChannel channel = new NotificationChannel("CHANNEL_ID", name, importance);
            channel.setDescription(description);
            NotificationManager notificationManager = getSystemService(NotificationManager.class);
            notificationManager.createNotificationChannel(channel);
        }
    }

    public class CreateNotify extends Thread{

        @Override
        public void run() {
            Notification notification=new NotificationCompat.Builder(MainActivity.this, "CHANNEL_ID")
                    .setSmallIcon(R.drawable.ic_baseline_warning_24)
                    .setContentTitle("Warning!")
                    .setContentText("Phát hiện ra lửa lúc " + Calendar.getInstance().getTime())
                    .setAutoCancel(true)
                    .build();
            NotificationManagerCompat notificationManager= NotificationManagerCompat.from(MainActivity.this);
            notificationManager.notify(iD_no,notification);
            iD_no++;
        }
    }
}