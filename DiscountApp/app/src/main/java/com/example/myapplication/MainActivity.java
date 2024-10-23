package com.example.myapplication;

import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import android.os.Bundle;
import android.os.Handler;
import android.os.StrictMode;
import android.widget.Button;
import android.widget.Toast;

import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.AbstractMap;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;
import java.util.Map;

public class MainActivity extends AppCompatActivity {

    private RecyclerView recyclerView;
    private DiscountAdapter discountAdapter;
    private List<Map.Entry<String, String>> discountList = new ArrayList<>(); // List to hold discount entries
    private Handler handler = new Handler();
    private final int REFRESH_INTERVAL = 30000; // 30 seconds refresh interval
    private boolean isFetching = false;  // Track whether fetching is ongoing

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        recyclerView = findViewById(R.id.recyclerView);
        recyclerView.setLayoutManager(new LinearLayoutManager(this));

        // Allow network operation on the main thread (not recommended, but okay for this example)
        StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();
        StrictMode.setThreadPolicy(policy);

        Button fetchButton = findViewById(R.id.fetchButton);
        fetchButton.setOnClickListener(v -> {
            if (isFetching) {
                stopFetchingData();  // Stop fetching if already fetching
                fetchButton.setText("Start Fetching");
            } else {
                startFetchingData();  // Start fetching if not already fetching
                fetchButton.setText("Stop Fetching");
            }
        });
    }

    private void startFetchingData() {
        isFetching = true;  // Update the fetching state
        handler.post(fetchDiscountsRunnable);  // Start the periodic task
    }

    private void stopFetchingData() {
        isFetching = false;  // Update the fetching state
        handler.removeCallbacks(fetchDiscountsRunnable);  // Stop fetching data
    }

    private final Runnable fetchDiscountsRunnable = new Runnable() {
        @Override
        public void run() {
            fetchDiscounts();  // Fetch data from the server
            handler.postDelayed(this, REFRESH_INTERVAL);  // Re-run after the specified interval
        }
    };

    private void fetchDiscounts() {
        try {
            // Replace with your JSONBin URL
            URL url = new URL("https://api.jsonbin.io/v3/b/6717ee52ad19ca34f8bcd76b");
            HttpURLConnection connection = (HttpURLConnection) url.openConnection();
            connection.setRequestMethod("GET");

            // Set the Master Key in the header
            connection.setRequestProperty("X-Master-Key", "$2a$10$Y2U9xKyBGfFloAihItxoK.4/UdvXE2frk.TS9Uz2zsLTFH1D8hND6");

            // Get the response
            BufferedReader in = new BufferedReader(new InputStreamReader(connection.getInputStream()));
            StringBuilder response = new StringBuilder();
            String inputLine;

            while ((inputLine = in.readLine()) != null) {
                response.append(inputLine);
            }
            in.close();

            // Parse the JSON response
            JSONObject jsonObject = new JSONObject(String.valueOf(response));
            JSONObject record = jsonObject.getJSONObject("record");

            discountList.clear(); // Clear previous discounts
            Iterator<String> keys = record.keys();

            while (keys.hasNext()) {
                String brand = keys.next();
                String offers = record.getString(brand);
                discountList.add(new AbstractMap.SimpleEntry<>(brand, offers));  // Add to the list as entries
            }

            // Set the adapter with the parsed data
            if (discountAdapter == null) {
                discountAdapter = new DiscountAdapter(this, discountList);  // Initialize the adapter with the list
                recyclerView.setAdapter(discountAdapter);
            } else {
                discountAdapter.notifyDataSetChanged();  // Notify the adapter of data changes
            }

        } catch (Exception e) {
            e.printStackTrace();
            Toast.makeText(this, "Error fetching data", Toast.LENGTH_SHORT).show();
        }
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        stopFetchingData();  // Ensure fetching stops when activity is destroyed
    }
}
