package com.example.demo.controller;

import com.example.demo.entity.LeaderHub;
import com.example.demo.repository.LeaderHubRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/leaderhub")
public class LeaderHubController {

    @Autowired
    private LeaderHubRepository leaderHubRepository;

    // Top scores list-ai edukka
    @GetMapping
    public List<LeaderHub> getLeaderboard() {
        return leaderHubRepository.findAllByOrderByScoreDesc();
    }

    // Puthiya score add panna
    @PostMapping
    public LeaderHub addScore(@RequestBody LeaderHub leaderHub) {
        return leaderHubRepository.save(leaderHub);
    }
}
