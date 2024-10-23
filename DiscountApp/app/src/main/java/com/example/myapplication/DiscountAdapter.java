package com.example.myapplication;

import android.content.Context;
import android.content.Intent;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import java.util.List;
import java.util.Map;

public class DiscountAdapter extends RecyclerView.Adapter<DiscountAdapter.DiscountViewHolder> {

    private List<Map.Entry<String, String>> discountList;
    private Context context;

    public DiscountAdapter(Context context, List<Map.Entry<String, String>> discountList) {
        this.context = context; // Initialize the context correctly
        this.discountList = discountList;
    }

    @NonNull
    @Override
    public DiscountViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View view = LayoutInflater.from(parent.getContext())
                .inflate(R.layout.brand_item_layout, parent, false); // Ensure this layout has CardView
        return new DiscountViewHolder(view);
    }

    @Override
    public void onBindViewHolder(@NonNull DiscountViewHolder holder, int position) {
        Map.Entry<String, String> discountEntry = discountList.get(position);
        String brandName = discountEntry.getKey();
        String discountOffer = discountEntry.getValue();

        holder.brandTextView.setText(brandName);
        holder.discountTextView.setText(discountOffer);

        // Set an OnClickListener on the item view
        holder.itemView.setOnClickListener(v -> {
            Intent intent = new Intent(context, DetailsActivity.class);
            intent.putExtra("BRAND_NAME", brandName);
            intent.putExtra("DISCOUNT_OFFER", discountOffer);
            context.startActivity(intent);
        });
    }

    @Override
    public int getItemCount() {
        return discountList.size();
    }

    public static class DiscountViewHolder extends RecyclerView.ViewHolder {
        TextView brandTextView;
        TextView discountTextView;

        public DiscountViewHolder(@NonNull View itemView) {
            super(itemView);
            brandTextView = itemView.findViewById(R.id.brandTextView);
            discountTextView = itemView.findViewById(R.id.discountTextView);
        }
    }
}
