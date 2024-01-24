package com.supercompta.manageldap.controller;

import com.supercompta.manageldap.model.User;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;

import javax.naming.Context;
import javax.naming.NamingEnumeration;
import javax.naming.NamingException;
import javax.naming.directory.*;
import java.util.ArrayList;
import java.util.List;
import java.util.Objects;
import java.util.Properties;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

@Controller
public class ManageLdap {
    DirContext connection;

    public void Connect() {
        Properties env = new Properties();
        env.put(Context.INITIAL_CONTEXT_FACTORY, "com.sun.jndi.ldap.LdapCtxFactory");
        env.put(Context.PROVIDER_URL, "ldap://dc1.supercompta.com:389");
        env.put(Context.SECURITY_PRINCIPAL, "cn=Administrator, cn=Users, dc=supercompta, dc=com");
        env.put(Context.SECURITY_CREDENTIALS, "Passw0rd");
        try {
            connection = new InitialDirContext(env);
            System.out.println("Connection successful");
        } catch (NamingException e) {
            e.printStackTrace();
        }
    }

    public String searchUsers(Model m) throws NamingException {
        Pattern patt = Pattern.compile("CN=([^,]*).*");
        List list_users = new ArrayList();
        SearchControls controls = new SearchControls();
        this.Connect();

        String searchFilter = "(memberOf=CN=Users,DC=supercompta,DC=com)";
        String[] requestAtt = {"CN", "memberOf"};
        controls.setSearchScope(SearchControls.SUBTREE_SCOPE);
        controls.setReturningAttributes(requestAtt);

        NamingEnumeration users = connection.search("CN=Users,DC=supercompta,DC=com", searchFilter, controls);

        SearchResult result = null;
        while (users.hasMore()) {
            result = (SearchResult) users.next();
            Attributes attr = result.getAttributes();
            String nom = attr.get("cn").get(0).toString();
            String groupe = "";

            User user = new User(nom, null);

            if (attr.get("memberOf") != null) {
                for(int i = 0; i <attr.get("memberOf").size(); i++){
                    Matcher match = patt.matcher(attr.get("memberOf").get(i).toString());
                    if(match.find()){
                        groupe += " "+ match.group(1);
                    }
                }
            }
            user.setGroupe(groupe);
            list_users.add(user);
        }
        m.addAttribute("users", list_users);
        return "actions";
    }


    // Debut du code couvrant la gestion des utilisateurs avec les mappings
    @GetMapping("/")
    public String welcome() {
        return "welcome";
    }

    @PostMapping("/ajouterUser")
    public String ajouter(){
        return "ajouterUser";
    }

    @PostMapping("/userLdap")
    public String addUser(User user, Model m) {
        try {
            this.Connect();
            System.out.println(user.getNom());
            System.out.println(user.getPrenom());
            System.out.println(user.getGroupe());
            user.setUsername(user.getPrenom().toLowerCase() + user.getNom().toLowerCase());

            String password = "P@ssw0rd";
            String basic_dn = ",DC=supercompta,DC=com";


            Attributes attributes = new BasicAttributes();
            Attribute attribute = new BasicAttribute("objectClass");
            attribute.add("user");

            attributes.put(attribute);
            // objectClass attributes
            attribute.add("top");
            attribute.add("person");
            attribute.add("user");
            attribute.add("organizationalPerson");

            // user info
            attributes.put(attribute);
            attributes.put("sn", user.getNom().toUpperCase());
            attributes.put("cn", user.getPrenom());
            attributes.put("givenName", user.getPrenom().toUpperCase());
            attributes.put("displayName", user.getPrenom().toUpperCase() + " " + user.getNom().toUpperCase());
            attributes.put("name", user.getUsername());
            attributes.put("sAMAccountName", user.getUsername());
            attributes.put("homeDirectory", "C:\\Users\\"+ user.getUsername());
            attributes.put("profilePath", "C:\\UserData\\"+ user.getUsername() +"\\profile");
            attributes.put("loginShell", "/bin/bash");
            attributes.put("unixHomeDirectory", "/home/"+ user.getUsername());

            if (Objects.equals(user.getGroupe(), "Management")) {
                attributes.put("gidNumber", "5000");
            } else if (Objects.equals(user.getGroupe(), "Techniciens")) {
                attributes.put("gidNumber", "5001");
            } else if (Objects.equals(user.getGroupe(), "RH")) {
                attributes.put("gidNumber", "5002");
            } else {
                attributes.put("gidNumber", "5003");
            }

            attributes.put("accountExpires", "0");
            attributes.put("userPassword", password);

            connection.createSubcontext("CN="+ user.getUsername() +",OU="+ user.getGroupe() + basic_dn, attributes);

            // Ajout au groupe
            ModificationItem[] mods = new ModificationItem[1];

            Attribute attribute2 = new BasicAttribute("member", "CN="+ user.getUsername() +",OU="+ user.getGroupe() +",DC=supercompta,DC=com");
            mods[0] = new ModificationItem(DirContext.ADD_ATTRIBUTE, attribute2);

            connection.modifyAttributes("CN="+ user.getGroupe() +", CN=Users" + basic_dn, mods);

            System.out.println("Added to group");
            System.out.println("User added successfully");

            return this.searchUsers(m);

        } catch (NamingException e) {
            e.printStackTrace();
            return "erreur";
        }

    }

    @PostMapping("/supprimerUser")
    public String deleteUser(User user, Model m)
    {
        try {
            this.Connect();
            System.out.println(user.getUsername());
            connection.destroySubcontext("CN="+ user.getUsername() +", OU="+ user.getGroupe() +", DC=supercompta, DC=com");
            return this.searchUsers(m);

        } catch (NamingException e) {
            e.printStackTrace();
            return "erreur";
        }
    }

    @PostMapping("/auth")
    public String authUser(User user, Model m)
    {
        try {
            this.Connect();

            System.out.println(user.getUsername());
            System.out.println(user.getPassword());
            Properties env = new Properties();

            env.put(Context.INITIAL_CONTEXT_FACTORY, "com.sun.jndi.ldap.LdapCtxFactory");
            env.put(Context.PROVIDER_URL, "ldap://dc1.supercompta.com:389");
            env.put(Context.SECURITY_PRINCIPAL, "cn="+ user.getUsername() +",OU=Techniciens, dc=supercompta, dc=com");
            env.put(Context.SECURITY_CREDENTIALS, user.getPassword());
            DirContext conn = new InitialDirContext(env);

            conn.close();
            return this.searchUsers(m);

        } catch (Exception e) {
            return "erreur";
        }
    }


}
