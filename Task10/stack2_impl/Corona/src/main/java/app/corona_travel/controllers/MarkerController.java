package app.corona_travel.controllers;

import org.json.JSONObject;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestBody;
import app.corona_travel.dao.ConditionsDao;

import java.util.ArrayList;

@Controller
public class MarkerController {

    private ConditionsDao dao;

    /**
     * Конструктор для внедрения зависимости
     * @param dao
     */
    @Autowired
    public MarkerController(ConditionsDao dao) {
        this.dao = dao;
    }

    @GetMapping("/test")
    public ResponseEntity<ArrayList<JSONObject>> answer(@RequestBody String gotXml) {
        ArrayList<JSONObject> markerInfo = dao.getMarkersInfo();
        return ResponseEntity.ok().contentType(MediaType.APPLICATION_JSON).body(markerInfo);
    }
}
