package com.UST.retails.service;

import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import com.UST.retails.repository.UserRepository;
import com.UST.retails.entity.User;

import java.util.List;

@Service
@RequiredArgsConstructor
public class UserService {

    private final UserRepository userRepository;

    public User save(User user) {
        return userRepository.save(user);
    }

    public List<User> getAll() {
        return userRepository.findAll();
    }
}