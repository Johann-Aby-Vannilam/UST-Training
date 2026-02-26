package com.UST.retails.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import com.UST.retails.entity.User;

public interface UserRepository extends JpaRepository<User, Long> {
}