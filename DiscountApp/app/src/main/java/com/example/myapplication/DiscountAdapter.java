package com.example.myapplication;

import android.content.Context;
import android.content.Intent;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;
import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

public class DiscountAdapter extends RecyclerView.Adapter<DiscountAdapter.DiscountViewHolder> {
    private Context context;
    private HashMap<String, String> discounts;
    private List<String> brandList;

    public DiscountAdapter(Context context, HashMap<String, String> discounts) {
        this.context = context;
        this.discounts = discounts;
        this.brandList = new ArrayList<>(discounts.keySet());  // Get the list of brand names
    }

    @Override
    public DiscountViewHolder onCreateViewHolder(ViewGroup parent, int viewType) {
        // Inflate your item_discount layout for each item
        View view = LayoutInflater.from(context).inflate(R.layout.item_discount, parent, false);
        return new DiscountViewHolder(view);
    }

    @Override
    public void onBindViewHolder(DiscountViewHolder holder, int position) {
        // Get the brand name and offers for the current position
        String brand = brandList.get(position);
        String offers = discounts.get(brand);

        // Set the data to the respective TextViews in the item layout
        holder.brandTextView.setText(brand);
        holder.offersTextView.setText(offers);

        // Set the click listener for the current item
        holder.itemView.setOnClickListener(v -> {
            Intent intent = new Intent(context, DetailsActivity.class);
            intent.putExtra("brand", brand);  // Pass the brand name to the details activity
            intent.putExtra("offers", offers);  // Pass the offers to the details activity
            context.startActivity(intent);  // Start the details activity
        });
    }

    @Override
    public int getItemCount() {
        return brandList.size();  // Return the size of the brand list
    }

    // ViewHolder class for the RecyclerView items
    public class DiscountViewHolder extends RecyclerView.ViewHolder {
        TextView brandTextView;
        TextView offersTextView;

        public DiscountViewHolder(View itemView) {
            super(itemView);
            // Find the TextViews in the item_discount layout
            brandTextView = itemView.findViewById(R.id.brandTextView);
            offersTextView = itemView.findViewById(R.id.discountTextView);
        }
    }
}
