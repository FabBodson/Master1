package com.supercompta.manageldap.model;

public class User {
    private String nom;
    private String prenom;
    private String username;
    private String groupe;
    private String password;

    // Sert à auth l'utilisateur
    public User(String username, String password){
        this.nom = null;
        this.prenom = null;
        this.username = username;
        this.password = password;
        this.groupe=null;
    }

    public String getNom() {
        return nom;
    }

    public String getPrenom() {
        return prenom;
    }

    public String getUsername(){ return username; }

    public void setUsername(String username) {
        this.username = username;
    }

    public String getGroupe() {
        return groupe;
    }

    public void setGroupe(String groupe) {
        this.groupe = groupe;
    }

    public String getPassword() {
        return password;
    }

}
