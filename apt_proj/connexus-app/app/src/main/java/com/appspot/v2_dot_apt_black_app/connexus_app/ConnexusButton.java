package com.appspot.v2_dot_apt_black_app.connexus_app;

import android.content.Context;
import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.Color;
import android.graphics.drawable.BitmapDrawable;
import android.graphics.drawable.Drawable;
import android.view.View;
import android.widget.LinearLayout;

import com.google.gson.JsonObject;

/**
 * Created by brice on 10/23/17.
 */

public class ConnexusButton extends android.support.v7.widget.AppCompatButton implements AsyncResponse
{
    String name;
    Context context;
    Drawable backGd;
    DownloadTask asyncTask = new DownloadTask();
    JsonObject json;
    Intent singleViewIntent;

    @Override
    public void processFinish(Drawable output){
        this.backGd = output;

        if(output == null)
        {
            return;
        }

        if(name.isEmpty()) {
            name = "";
        }
        /* I did try to go the drawable route...
        //TODO: revisit if we have time to make text over images more readable
        Bitmap canvasBitmap = Bitmap.createBitmap(backGd.getIntrinsicWidth(), backGd.getIntrinsicHeight(),
                Bitmap.Config.ARGB_8888);
        // Create a canvas, that will draw on to canvasBitmap.
        Canvas imageCanvas = new Canvas(canvasBitmap);
        // Set up the paint for use with our Canvas
        Paint imagePaint = new Paint();
        imagePaint.setTextAlign(Paint.Align.CENTER);
        imagePaint.setTextSize(16f);
        // Draw the image to our canvas
        output.draw(imageCanvas);
        // Draw the text on top of our image
        imageCanvas.drawText(name, backGd.getIntrinsicWidth() / 2,
                backGd.getIntrinsicHeight() / 2,
                imagePaint);
        // Combine background and text to a LayerDrawable
        LayerDrawable layerDrawable = new LayerDrawable(
                new Drawable[]{output,
                        new BitmapDrawable(context.getResources(), canvasBitmap)}
        );
        Drawable myDrawable = new BitmapDrawable(context.getResources(), canvasBitmap);
        */

        Bitmap b = ((BitmapDrawable)backGd).getBitmap();
        //layerDrawable.draw(new Canvas(b));
        //backGd.draw(new Canvas(b));

        Bitmap bitmapResized = Bitmap.createScaledBitmap(b, 225, 225, false);
        this.setBackgroundDrawable(new BitmapDrawable(getResources(), bitmapResized));
    }

    public ConnexusButton(final Context con, JsonObject jObj, Intent intent)
    {
        super(con);
        this.context = con;
        json = jObj;
        singleViewIntent = intent;

        if(json != null)
        {
            int len = 10;
            name = json.get("stream_name").toString();
            if(name.length() > len)
            {
                name = name.substring(0, len+1);
            }
            if (json.get("cover_image").getAsString().replace("\"", "").length() > 0) {
                asyncTask.delegate = this;
                asyncTask.execute(json.get("cover_image").getAsString().replace("\"", ""));
            }
            if (json.get("distance") != null && !json.get("distance").toString().equals("null")) {
                String dist = json.get("distance").toString();
                int size = dist.length();
                if (size > 8) {
                    size = 8;
                }
                this.setText(dist.substring(0,size));
            } else {
                int size = name.length();
                if (size > 8) {
                    size = 8;
                }
                this.setText(name.substring(0, size));
            }
            this.setTextColor(Color.WHITE);
            this.setBackgroundColor(Color.TRANSPARENT);
        }
        else
        {
            this.setBackgroundColor(Color.TRANSPARENT);
            setClickable(false);
            return;
        }

        /*
            A JsonObject has the following structure:
            {
                "stream_name":"basketball",
                "key_url":"ag9zfmFwdC1ibGFjay1hcHByEwsSBlN0cmVhbRiAgICAvJ-bCgw",
                "subscribers":[],
                "cover_image":"https://i5.walmartimages.com/asr/d0f3658b-3cf8-459d-ad14-f300c2495836_1.4287fec35da69e2633d03c7f46990a56.jpeg?odnHeight=450&odnWidth=450&odnBg=FFFFFF",
                "key_id":"5700305828184064",
                "owner":"vasic@utexas.edu"
            }

                   Store the image on the phone with name the cover url.
         */
        this.setClickable(true);
        this.setLayoutParams(new LinearLayout.LayoutParams(LinearLayout.LayoutParams.MATCH_PARENT, LinearLayout.LayoutParams.WRAP_CONTENT, 1.0f));

        this.setOnClickListener(new OnClickListener() {
            @Override
            public void onClick(View view)
            {
                singleViewIntent.setClass(context, SingleStreamActivity.class);
                singleViewIntent.putExtra("stream_name", name = json.get("stream_name").getAsString().replace("\"", ""));
                singleViewIntent.putExtra("owner", name = json.get("owner").getAsString().replace("\"", ""));
                singleViewIntent.putExtra("key_url", name = json.get("key_url").getAsString().replace("\"", ""));
                singleViewIntent.putExtra("key_id", name = json.get("key_id").getAsString().replace("\"", ""));
                context.startActivity(singleViewIntent);
            }
        });
    }

}
