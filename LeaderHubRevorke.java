package com.example.demo.entity;

import jakarta.persistence.*;

@Entity
@Table(name = "leader_hub")
public class LeaderHub {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String username;
    private int score;

    public LeaderHub() {}

    public LeaderHub(String username, int score) {
        this.username = username;
        this.score = score;
    }

    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    public String getUsername() { return username; }
    public void setUsername(String username) { this.username = username; }
    public int getScore() { return score; }
    public void setScore(int score) { this.score = score; }
}
