package com.appspot.v2_dot_apt_black_app.connexus_app;

import android.content.Context;
import android.content.Intent;
import android.graphics.drawable.Drawable;
import android.util.Log;
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

    @Override
    public void processFinish(Drawable output){
        this.backGd = output;
        this.setBackgroundDrawable(output);
    }

    public ConnexusButton(final Context con, JsonObject jObj)
    {
        super(con);
        this.context = con;

        if(jObj != null)
        {
            int len = 10;
            name = jObj.get("stream_name").toString();
            if(name.length() > len)
            {
                name = name.substring(0, len+1);
            }

            this.setText(name);
            this.setTextSize(8);
            Log.i("=> ", jObj.toString());
            asyncTask.delegate = this;
            asyncTask.execute(jObj.get("cover_image").getAsString().replace("\"", ""));
        }
        else
        {
            this.setText("Empty");
            this.setTextSize(8);
            this.setClickable(true);
            Log.i("=> ", "NULL OBJ");
        }

        /*
            A JsonObject has the following structure:
            {
                "stream_name":"basketball",
                "key_kind":"Stream",
                "subscribers":[],
                "cover_image":"https://i5.walmartimages.com/asr/d0f3658b-3cf8-459d-ad14-f300c2495836_1.4287fec35da69e2633d03c7f46990a56.jpeg?odnHeight=450&odnWidth=450&odnBg=FFFFFF",
                "key_id":"5700305828184064",
                "owner":"vasic@utexas.edu"
            }

                   Store the image on the phone with name the cover url.
         */
        this.setLayoutParams(new LinearLayout.LayoutParams(LinearLayout.LayoutParams.MATCH_PARENT, LinearLayout.LayoutParams.WRAP_CONTENT, 1.0f));

        this.setOnClickListener(new OnClickListener() {
            @Override
            public void onClick(View view)
            {
                Intent singleViewIntent = new Intent(context, SingleStreamActivity.class);
                //TODO: Pass in the necessary data to this intent before going to the single button activity
                context.startActivity(singleViewIntent);
            }
        });
    }

}