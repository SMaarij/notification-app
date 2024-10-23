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
        String brand = intent.getStringExtra("BRAND_NAME");  // Use the correct key
        String offers = intent.getStringExtra("DISCOUNT_OFFER");  // Use the correct key

        // Set the brand and offers in TextViews
        TextView brandTextView = findViewById(R.id.brandTextView);
        TextView offersTextView = findViewById(R.id.offersTextView);

        brandTextView.setText(brand);
        offersTextView.setText(offers);

        // Add a button for visiting the brand website
        Button visitButton = findViewById(R.id.visitWebsiteButton);
        visitButton.setOnClickListener(v -> {
            // Get the brand URL and open it in a browser
            String url = getBrandWebsiteUrl(brand);  // Get the URL based on the brand name
            Intent browserIntent = new Intent(Intent.ACTION_VIEW, Uri.parse(url));
            startActivity(browserIntent);
        });
    }

    // This method returns the brand's website URL based on the brand name
    private String getBrandWebsiteUrl(String brand) {
        switch (brand) {
            case "Junaid Jamshed":
                return "https://www.junaidjamshed.com/";
            case "Brand B":
                return "https://www.brandb.com";  // Update with the actual URL
            // Add more cases for other brands as needed
            default:
                return "https://www.default-brand.com";  // Default URL
        }
    }
}
