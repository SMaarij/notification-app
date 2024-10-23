package com.example.myapplication;

import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.widget.Button;
import android.widget.TextView;
import androidx.appcompat.app.AppCompatActivity;

public class DetailsActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_details);

        // Get the brand and offers from the Intent
        Intent intent = getIntent();
        String brand = intent.getStringExtra("brand");
        String offers = intent.getStringExtra("offers");

        // Set the brand and offers in TextViews
        TextView brandTextView = findViewById(R.id.brandTextView);
        TextView offersTextView = findViewById(R.id.offersTextView);

        brandTextView.setText(brand);
        offersTextView.setText(offers);

        // Add a button for visiting the brand website
        Button visitButton = findViewById(R.id.visitWebsiteButton);
        visitButton.setOnClickListener(v -> {
            // Assuming you have the brand URL saved somewhere
            String url = getBrandWebsiteUrl(brand);  // You need to implement this method to get the URL
            Intent browserIntent = new Intent(Intent.ACTION_VIEW, Uri.parse(url));
            startActivity(browserIntent);
        });
    }

    // This method should return the brand's website URL based on the brand name
    private String getBrandWebsiteUrl(String brand) {
        // You can use a map or a switch statement to return URLs based on the brand name
        switch (brand) {
            case "Junaid Jamshed":
                return "https://www.junaidjamshed.com/";
            case "Brand B":
                return "https://www.junaidjamshed.com";
            default:
                return "https://www.default-brand.com";  // Default URL
        }
    }
}
