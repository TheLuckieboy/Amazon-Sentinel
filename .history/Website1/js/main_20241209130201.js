document.addEventListener("DOMContentLoaded", function () {
    // Select the input element and the search button
    const idInputField = document.getElementById('formField114-1733328551164-4247');
    const loginInputField = document.getElementById('formField113-1733328551163-6001');
    const searchButton = document.querySelector('button[data-analytics-funnel-value="button130-1733328551171-3358"]');

    // Function to perform search based on input type
    function performSearch() {
        const idInputValue = idInputField.value.trim();
        const loginInputValue = loginInputField.value.trim();

        if (!idInputValue && !loginInputValue) {
            console.log("Please enter an Employee ID or Login.");
            return;
        }

        console.log("Performing search...");
        fetch('http://localhost:3000/profiles.json')
            .then(response => response.json())
            .then(profiles => {
                let profile = null;

                if (idInputValue) {
                    profileData = profiles.find(p => p.Employee_ID === idInputValue);
                } else if (loginInputValue) {
                    profileData = profiles.find(p => p.Login === loginInputValue);
                }

                if (profileData) {
                    console.log('Found profile:', profileData);
                    displayProfile(profileData);
                } else {
                    console.log('Profile not found.');
                }
            })
            .catch(error => {
                console.error('Error fetching profiles:', error);
            });
    }

    /*function displayProfile(profile) {
        console.log("Profile Information:");
        console.log(`Login: ${profile.Login}`);
        console.log(`Employee ID: ${profile.Employee_ID}`);
        console.log(`Person ID: ${profile.Person_ID}`);
        console.log(`Name: ${profile.First_Name} ${profile.Last_Name}`);
        console.log(`Type: ${profile.Employee_Type}`);
        console.log(`Status: ${profile.Employee_Status}`);
        console.log(`Manager: ${profile.Manager}`);
        console.log(`Tenure: ${profile.Tenure}`);
        console.log(`Region: ${profile.Region}`);
        console.log(`Building/Country: ${profile["Building/Country"]}`);
        console.log(`Badge Count: ${profile.Badge_Count}`);
        console.log("Badges:");
        profile.Badges.forEach((badge, index) => {
            console.log(`  Badge ${index + 1}:`);
            console.log(`    ID: ${badge.Badge_ID}`);
            console.log(`    Status: ${badge.Badge_Status}`);
            console.log(`    Type: ${badge.Badge_Type}`);
            console.log(`    Activate On: ${badge.Badge_ActivateOn}`);
            console.log(`    Deactivate On: ${badge.Badge_DeactivateOn}`);
            console.log(`    Last Updated: ${badge.Badge_LastUpdatedUTC}`);
            console.log(`    Last Location Reader Name: ${badge.Badge_LastLocationReaderName}`);
            console.log(`    Last Location Event Type: ${badge.Badge_LastLocationEventType}`);
        });
        console.log(`Access Level Count: ${profile.AccessLvl_Count}`);
        console.log("Access Levels:");
        profile.AccessLvl.forEach((access, index) => {
            console.log(`  Access Level ${index + 1}:`);
            console.log(`    Level: ${access.AccessLevel}`);
            console.log(`    Activate On: ${access.AccessLevel_ActivateOn}`);
            console.log(`    Deactivate On: ${access.AccessLevel_Deactivate}`);
        });
    }*/


    // Function to display the profile data
    function displayProfile(profileData) {
        // Find the main parent container
        const parentElement = document.querySelector('.awsui_root_18582_7onux_141.awsui_vertical_18582_7onux_188.awsui_vertical-xs_18582_7onux_197');

        if (!parentElement) {
            console.error('Parent element not found');
            return;
        }

        // Check if a profile section already exists
        let profileSection = Array.from(parentElement.children).find(
            child => child.classList.contains('profile-section')
        );

        if (!profileSection) {
            // Create a new child container for the profile
            profileSection = document.createElement('div');
            profileSection.classList.add('awsui_child_18582_7onux_145', 'profile-section'); // Add required class and a unique identifier
            parentElement.appendChild(profileSection);
        } else {
            // Clear existing content
            profileSection.innerHTML = '';
        }

        // Generate a random image URL using DiceBear
        const randomSeed = Math.random().toString(36).substring(7); // Generate a random seed
        const styles = ['adventurer', 'adventurer-neutral', 'avataaars', 'avataaars-neutral', 'big-ears', 'big-ears-neutral', 'big-smile', 'bottts', 'bottts-neutral'];
        const randomStyle = styles[Math.floor(Math.random() * styles.length)]; // Randomly select a style
        const profileImage = `https://api.dicebear.com/6.x/${randomStyle}/svg?seed=${randomSeed}`; // Use "bottts" style for random avatars

        const BadgeData = generateBadgeTableHTML(profileData)

        // Add the profile data as inner HTML
        profileSection.innerHTML = `
            <div class="awsui_root_18582_7onux_141 awsui_vertical_18582_7onux_188 awsui_vertical-xxxs_18582_7onux_191">
                <div class="awsui_child_18582_7onux_145">
                    <div class="awsui_root_14iqq_zuudq_185 awsui_variant-default_14iqq_zuudq_229">
                        <div id="12471-1733498994777-8445" class="awsui_content-wrapper_14iqq_zuudq_304">
                            <div class="awsui_header_14iqq_zuudq_345 awsui_header_164jl_1ns0c_5 awsui_with-paddings_14iqq_zuudq_388">
                                <div class="awsui_root_2qdw9_kiqfw_177 awsui_root-variant-h1_2qdw9_kiqfw_228 awsui_root-no-actions_2qdw9_kiqfw_216">
                                    <div class="awsui_main_2qdw9_kiqfw_238 awsui_main-variant-h1_2qdw9_kiqfw_254">
                                        <div class="awsui_title_2qdw9_kiqfw_294 awsui_title-variant-h1_2qdw9_kiqfw_299">
                                            <h1 class="awsui_heading_2qdw9_kiqfw_370 awsui_heading-variant-h1_2qdw9_kiqfw_381"><span data-analytics-funnel-key="substep-name" class="awsui_heading-text_2qdw9_kiqfw_397 awsui_heading-text_105ke_268sp_5 awsui_heading-text-variant-h1_2qdw9_kiqfw_400" id="heading12472-1733498994777-1727">${profileData.Last_Name || ''}, ${profileData.First_Name || ''} (${profileData.Login || ''})</span></h1></div>
                                    </div>
                                </div>
                            </div>
                            <div class="awsui_content_14iqq_zuudq_304">
                                <div class="awsui_content-inner_14iqq_zuudq_492 awsui_content-inner_1mwlm_oyjaq_5 awsui_with-paddings_14iqq_zuudq_388 awsui_with-header_14iqq_zuudq_499">
                                    <div class="awsui_column-layout_vvxn7_43x2e_177">
                                        <div class="awsui_grid_14yj0_1cgl1_141 awsui_grid_vvxn7_43x2e_212 awsui_grid-columns-4_vvxn7_43x2e_251 awsui_grid-variant-text-grid_vvxn7_43x2e_222 awsui_no-gutters_14yj0_1cgl1_180 awsui_grid-breakpoint-xs_vvxn7_43x2e_236">
                                            <div class="awsui_grid-column_14yj0_1cgl1_185 awsui_colspan-3_14yj0_1cgl1_216">
                                                <div class="awsui_restore-pointer-events_14yj0_1cgl1_356">
                                                    <div style="width: 260px; height: auto; display: flex; align-self: auto; flex-direction: column; justify-content: center; align-items: center; margin: 10px;">
                                                        <div class="awsui_root_18582_7onux_141 awsui_vertical_18582_7onux_188 awsui_vertical-xs_18582_7onux_197">
                                                            <div class="awsui_child_18582_7onux_145"><img src="${profileImage}" alt="Cardholder badge photo" style="max-width: 50%; max-height: 60%; border-radius: 10px; margin: auto; align-items: center; display: flex; justify-content: center;"></div>
                                                            <div class="awsui_child_18582_7onux_145">
                                                                <div class="awsui_root_18582_7onux_141 awsui_horizontal_18582_7onux_156 awsui_horizontal-xxs_18582_7onux_163">
                                                                    <div class="awsui_child_18582_7onux_145"><span style="display: flex; flex-direction: row; justify-content: center; align-items: center;"><button class="awsui_button_vjswe_4v1qr_153 awsui_variant-normal_vjswe_4v1qr_204" data-analytics-funnel-value="button12486-1733498994783-3135" type="submit" data-analytics-performance-mark="12487-1733498994783-6000"><span class="awsui_content_vjswe_4v1qr_149 awsui_label_1f1d4_ocied_5"><div class="awsui_text-content_6absk_1e02k_142"><p style="font-size: 12px; font-weight: bold; cursor: pointer; flex: 1 1 0%;">Upload Photo</p></div></span></button>
                                                                        <button class="awsui_button_vjswe_4v1qr_153 awsui_variant-normal_vjswe_4v1qr_204 awsui_button-no-wrap_vjswe_4v1qr_1137" data-analytics-funnel-value="button12489-1733498994783-3819" type="submit" data-analytics-performance-mark="12490-1733498994783-3039"><span class="awsui_content_vjswe_4v1qr_149 awsui_label_1f1d4_ocied_5"><div class="awsui_text-content_6absk_1e02k_142"><p style="font-size: 12px; font-weight: bold; cursor: pointer; flex: 1 1 0%;">Take Photo</p></div></span></button>
                                                                        <button class="awsui_button_vjswe_4v1qr_153 awsui_variant-normal_vjswe_4v1qr_204" data-analytics-funnel-value="button12492-1733498994783-6026" type="submit" data-analytics-performance-mark="12493-1733498994783-9590"><span class="awsui_content_vjswe_4v1qr_149 awsui_label_1f1d4_ocied_5"><div class="awsui_text-content_6absk_1e02k_142"><p style="font-size: 12px; font-weight: bold; cursor: pointer; flex: 1 1 0%;">Select Photo</p></div></span></button>
                                                                        </span>
                                                                    </div>
                                                                </div>
                                                            </div>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                            <div class="awsui_grid-column_14yj0_1cgl1_185 awsui_colspan-3_14yj0_1cgl1_216">
                                                <div class="awsui_restore-pointer-events_14yj0_1cgl1_356">
                                                    <div>
                                                        <div class="awsui_root_18582_7onux_141 awsui_vertical_18582_7onux_188 awsui_vertical-xl_18582_7onux_209">
                                                            <div class="awsui_child_18582_7onux_145">
                                                                <div>
                                                                    <div class="awsui_root_18582_7onux_141 awsui_vertical_18582_7onux_188 awsui_vertical-xs_18582_7onux_197">
                                                                        <div class="awsui_child_18582_7onux_145">
                                                                            <div class="awsui_root_18wu0_1lw09_916 awsui_box_18wu0_1lw09_168 awsui_color-text-label_18wu0_1lw09_295 awsui_font-size-body-m_18wu0_1lw09_324 awsui_font-weight-bold_18wu0_1lw09_363">Login:</div>
                                                                        </div>
                                                                        <div class="awsui_child_18582_7onux_145">
                                                                            <div class="awsui_root_2rhyz_oflk9_141 awsui_input-container_2rhyz_oflk9_309">
                                                                                <input class="awsui_input_2rhyz_oflk9_145 awsui_input-readonly_2rhyz_oflk9_195" autocomplete="on" readonly="" type="text" value="${profileData.Login || ''}">
                                                                            </div>
                                                                        </div>
                                                                    </div>
                                                                </div>
                                                            </div>
                                                            <div class="awsui_child_18582_7onux_145">
                                                                <div>
                                                                    <div class="awsui_root_18582_7onux_141 awsui_vertical_18582_7onux_188 awsui_vertical-xs_18582_7onux_197">
                                                                        <div class="awsui_child_18582_7onux_145">
                                                                            <div class="awsui_root_18wu0_1lw09_916 awsui_box_18wu0_1lw09_168 awsui_color-text-label_18wu0_1lw09_295 awsui_font-size-body-m_18wu0_1lw09_324 awsui_font-weight-bold_18wu0_1lw09_363">Employee ID:</div>
                                                                        </div>
                                                                        <div class="awsui_child_18582_7onux_145">
                                                                            <div class="awsui_root_2rhyz_oflk9_141 awsui_input-container_2rhyz_oflk9_309">
                                                                                <input class="awsui_input_2rhyz_oflk9_145 awsui_input-readonly_2rhyz_oflk9_195" autocomplete="on" readonly="" type="text" value="${profileData.Employee_ID || ''}">
                                                                            </div>
                                                                        </div>
                                                                    </div>
                                                                </div>
                                                            </div>
                                                            <div class="awsui_child_18582_7onux_145">
                                                                <div>
                                                                    <div class="awsui_root_18582_7onux_141 awsui_vertical_18582_7onux_188 awsui_vertical-xs_18582_7onux_197">
                                                                        <div class="awsui_child_18582_7onux_145">
                                                                            <div class="awsui_root_18wu0_1lw09_916 awsui_box_18wu0_1lw09_168 awsui_color-text-label_18wu0_1lw09_295 awsui_font-size-body-m_18wu0_1lw09_324 awsui_font-weight-bold_18wu0_1lw09_363">Person ID:</div>
                                                                        </div>
                                                                        <div class="awsui_child_18582_7onux_145">
                                                                            <div class="awsui_root_2rhyz_oflk9_141 awsui_input-container_2rhyz_oflk9_309">
                                                                                <input class="awsui_input_2rhyz_oflk9_145 awsui_input-readonly_2rhyz_oflk9_195" autocomplete="on" readonly="" type="text" value="${profileData.Person_ID || ''}">
                                                                            </div>
                                                                        </div>
                                                                    </div>
                                                                </div>
                                                            </div>
                                                            <div class="awsui_child_18582_7onux_145">
                                                                <div>
                                                                    <div class="awsui_root_18582_7onux_141 awsui_vertical_18582_7onux_188 awsui_vertical-xs_18582_7onux_197">
                                                                        <div class="awsui_child_18582_7onux_145">
                                                                            <div class="awsui_root_18wu0_1lw09_916 awsui_box_18wu0_1lw09_168 awsui_color-text-label_18wu0_1lw09_295 awsui_font-size-body-m_18wu0_1lw09_324 awsui_font-weight-bold_18wu0_1lw09_363">Barcode:</div>
                                                                        </div>
                                                                        <div class="awsui_child_18582_7onux_145">
                                                                            <div class="awsui_root_2rhyz_oflk9_141 awsui_input-container_2rhyz_oflk9_309">
                                                                                <input class="awsui_input_2rhyz_oflk9_145 awsui_input-readonly_2rhyz_oflk9_195" autocomplete="on" readonly="" type="text" value="${profileData.Barcode || ''}">
                                                                            </div>
                                                                        </div>
                                                                    </div>
                                                                </div>
                                                            </div>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                            <div class="awsui_grid-column_14yj0_1cgl1_185 awsui_colspan-3_14yj0_1cgl1_216">
                                                <div class="awsui_restore-pointer-events_14yj0_1cgl1_356">
                                                    <div>
                                                        <div class="awsui_root_18582_7onux_141 awsui_vertical_18582_7onux_188 awsui_vertical-xl_18582_7onux_209">
                                                            <div class="awsui_child_18582_7onux_145">
                                                                <div>
                                                                    <div class="awsui_root_18582_7onux_141 awsui_vertical_18582_7onux_188 awsui_vertical-xs_18582_7onux_197">
                                                                        <div class="awsui_child_18582_7onux_145">
                                                                            <div class="awsui_root_18wu0_1lw09_916 awsui_box_18wu0_1lw09_168 awsui_color-text-label_18wu0_1lw09_295 awsui_font-size-body-m_18wu0_1lw09_324 awsui_font-weight-bold_18wu0_1lw09_363">First Name:</div>
                                                                        </div>
                                                                        <div class="awsui_child_18582_7onux_145">
                                                                            <div class="awsui_root_2rhyz_oflk9_141 awsui_input-container_2rhyz_oflk9_309">
                                                                                <input class="awsui_input_2rhyz_oflk9_145 awsui_input-readonly_2rhyz_oflk9_195" autocomplete="on" readonly="" type="text" value="${profileData.First_Name || ''}">
                                                                            </div>
                                                                        </div>
                                                                    </div>
                                                                </div>
                                                            </div>
                                                            <div class="awsui_child_18582_7onux_145">
                                                                <div>
                                                                    <div class="awsui_root_18582_7onux_141 awsui_vertical_18582_7onux_188 awsui_vertical-xs_18582_7onux_197">
                                                                        <div class="awsui_child_18582_7onux_145">
                                                                            <div class="awsui_root_18wu0_1lw09_916 awsui_box_18wu0_1lw09_168 awsui_color-text-label_18wu0_1lw09_295 awsui_font-size-body-m_18wu0_1lw09_324 awsui_font-weight-bold_18wu0_1lw09_363">Last Name:</div>
                                                                        </div>
                                                                        <div class="awsui_child_18582_7onux_145">
                                                                            <div class="awsui_root_2rhyz_oflk9_141 awsui_input-container_2rhyz_oflk9_309">
                                                                                <input class="awsui_input_2rhyz_oflk9_145 awsui_input-readonly_2rhyz_oflk9_195" autocomplete="on" readonly="" type="text" value="${profileData.Last_Name || ''}">
                                                                            </div>
                                                                        </div>
                                                                    </div>
                                                                </div>
                                                            </div>
                                                            <div class="awsui_child_18582_7onux_145">
                                                                <div>
                                                                    <div class="awsui_root_18582_7onux_141 awsui_vertical_18582_7onux_188 awsui_vertical-xs_18582_7onux_197">
                                                                        <div class="awsui_child_18582_7onux_145">
                                                                            <div class="awsui_root_18wu0_1lw09_916 awsui_box_18wu0_1lw09_168 awsui_color-text-label_18wu0_1lw09_295 awsui_font-size-body-m_18wu0_1lw09_324 awsui_font-weight-bold_18wu0_1lw09_363">Employee Type:</div>
                                                                        </div>
                                                                        <div class="awsui_child_18582_7onux_145">
                                                                            <div class="awsui_root_2rhyz_oflk9_141 awsui_input-container_2rhyz_oflk9_309">
                                                                                <input class="awsui_input_2rhyz_oflk9_145 awsui_input-readonly_2rhyz_oflk9_195" autocomplete="on" readonly="" type="text" value="${profileData.Employee_Type || ''}">
                                                                            </div>
                                                                        </div>
                                                                    </div>
                                                                </div>
                                                            </div>
                                                            <div class="awsui_child_18582_7onux_145">
                                                                <div>
                                                                    <div class="awsui_root_18582_7onux_141 awsui_vertical_18582_7onux_188 awsui_vertical-xs_18582_7onux_197">
                                                                        <div class="awsui_child_18582_7onux_145">
                                                                            <div class="awsui_root_18wu0_1lw09_916 awsui_box_18wu0_1lw09_168 awsui_color-text-label_18wu0_1lw09_295 awsui_font-size-body-m_18wu0_1lw09_324 awsui_font-weight-bold_18wu0_1lw09_363">Employee Status:</div>
                                                                        </div>
                                                                        <div class="awsui_child_18582_7onux_145">
                                                                            <div class="awsui_root_2rhyz_oflk9_141 awsui_input-container_2rhyz_oflk9_309">
                                                                                <input class="awsui_input_2rhyz_oflk9_145 awsui_input-readonly_2rhyz_oflk9_195" autocomplete="on" readonly="" type="text" value="${profileData.Employee_Status || ''}">
                                                                            </div>
                                                                        </div>
                                                                    </div>
                                                                </div>
                                                            </div>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                            <div class="awsui_grid-column_14yj0_1cgl1_185 awsui_colspan-3_14yj0_1cgl1_216">
                                                <div class="awsui_restore-pointer-events_14yj0_1cgl1_356">
                                                    <div>
                                                        <div class="awsui_root_18582_7onux_141 awsui_vertical_18582_7onux_188 awsui_vertical-xl_18582_7onux_209">
                                                            <div class="awsui_child_18582_7onux_145">
                                                                <div>
                                                                    <div class="awsui_root_18582_7onux_141 awsui_vertical_18582_7onux_188 awsui_vertical-xs_18582_7onux_197">
                                                                        <div class="awsui_child_18582_7onux_145">
                                                                            <div class="awsui_root_18wu0_1lw09_916 awsui_box_18wu0_1lw09_168 awsui_color-text-label_18wu0_1lw09_295 awsui_font-size-body-m_18wu0_1lw09_324 awsui_font-weight-bold_18wu0_1lw09_363">Manager:</div>
                                                                        </div>
                                                                        <div class="awsui_child_18582_7onux_145">
                                                                            <div class="awsui_root_2rhyz_oflk9_141 awsui_input-container_2rhyz_oflk9_309">
                                                                                <input class="awsui_input_2rhyz_oflk9_145 awsui_input-readonly_2rhyz_oflk9_195" autocomplete="on" readonly="" type="text" value="${profileData.Manager || ''}">
                                                                            </div>
                                                                        </div>
                                                                    </div>
                                                                </div>
                                                            </div>
                                                            <div class="awsui_child_18582_7onux_145">
                                                                <div>
                                                                    <div class="awsui_root_18582_7onux_141 awsui_vertical_18582_7onux_188 awsui_vertical-xs_18582_7onux_197">
                                                                        <div class="awsui_child_18582_7onux_145">
                                                                            <div class="awsui_root_18wu0_1lw09_916 awsui_box_18wu0_1lw09_168 awsui_color-text-label_18wu0_1lw09_295 awsui_font-size-body-m_18wu0_1lw09_324 awsui_font-weight-bold_18wu0_1lw09_363">Tenure:</div>
                                                                        </div>
                                                                        <div class="awsui_child_18582_7onux_145">
                                                                            <div class="awsui_root_2rhyz_oflk9_141 awsui_input-container_2rhyz_oflk9_309">
                                                                                <input class="awsui_input_2rhyz_oflk9_145 awsui_input-readonly_2rhyz_oflk9_195" autocomplete="on" readonly="" type="text" value="${profileData.Tenure || ''}">
                                                                            </div>
                                                                        </div>
                                                                    </div>
                                                                </div>
                                                            </div>
                                                            <div class="awsui_child_18582_7onux_145">
                                                                <div>
                                                                    <div class="awsui_root_18582_7onux_141 awsui_vertical_18582_7onux_188 awsui_vertical-xs_18582_7onux_197">
                                                                        <div class="awsui_child_18582_7onux_145">
                                                                            <div class="awsui_root_18wu0_1lw09_916 awsui_box_18wu0_1lw09_168 awsui_color-text-label_18wu0_1lw09_295 awsui_font-size-body-m_18wu0_1lw09_324 awsui_font-weight-bold_18wu0_1lw09_363">Region:</div>
                                                                        </div>
                                                                        <div class="awsui_child_18582_7onux_145">
                                                                            <div class="awsui_root_2rhyz_oflk9_141 awsui_input-container_2rhyz_oflk9_309">
                                                                                <input class="awsui_input_2rhyz_oflk9_145 awsui_input-readonly_2rhyz_oflk9_195" autocomplete="on" readonly="" type="text" value="${profileData.Region || ''}">
                                                                            </div>
                                                                        </div>
                                                                    </div>
                                                                </div>
                                                            </div>
                                                            <div class="awsui_child_18582_7onux_145">
                                                                <div>
                                                                    <div class="awsui_root_18582_7onux_141 awsui_vertical_18582_7onux_188 awsui_vertical-xs_18582_7onux_197">
                                                                        <div class="awsui_child_18582_7onux_145">
                                                                            <div class="awsui_root_18wu0_1lw09_916 awsui_box_18wu0_1lw09_168 awsui_color-text-label_18wu0_1lw09_295 awsui_font-size-body-m_18wu0_1lw09_324 awsui_font-weight-bold_18wu0_1lw09_363">Building/Country:</div>
                                                                        </div>
                                                                        <div class="awsui_child_18582_7onux_145">
                                                                            <div class="awsui_root_2rhyz_oflk9_141 awsui_input-container_2rhyz_oflk9_309">
                                                                                <input class="awsui_input_2rhyz_oflk9_145 awsui_input-readonly_2rhyz_oflk9_195" autocomplete="on" readonly="" type="text" value="${profileData.Building_Country || ''}">
                                                                            </div>
                                                                        </div>
                                                                    </div>
                                                                </div>
                                                            </div>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="awsui_child_18582_7onux_145">
                    <div class="awsui_root_14rmt_pykih_501 awsui_root_14iqq_zuudq_185 awsui_variant-default_14iqq_zuudq_229">
                        <div id="12474-1733498994778-9839" class="awsui_content-wrapper_14iqq_zuudq_304">
                            <div class="awsui_header_14iqq_zuudq_345 awsui_header_164jl_1ns0c_5">
                                <div class="awsui_tabs-header_14rmt_pykih_282">
                                    <ul role="tablist" class="awsui_tabs-header-list_14rmt_pykih_290 awsui_tabs-header-list_1acwa_dp0cl_5">
                                        <li class="awsui_tabs-tab_14rmt_pykih_329" role="presentation">
                                            <div class="awsui_tabs-tab-header-container_14rmt_pykih_349 awsui_tabs-tab-active_14rmt_pykih_486 awsui_tabs-tab-focusable_14rmt_pykih_497">
                                                <button class="awsui_tabs-tab-link_14rmt_pykih_410 awsui_tabs-tab-active_14rmt_pykih_486 awsui_tabs-tab-focused_14rmt_pykih_592 awsui_active-tab-header_1acwa_dp0cl_6 awsui_tabs-tab-focusable_14rmt_pykih_497" aria-controls="awsui-tabs-12473-1733498994778-9458-second-panel" data-testid="second" id="awsui-tabs-12473-1733498994778-9458-second" aria-selected="true" role="tab" tabindex="0" type="button"><span class="awsui_tabs-tab-label_14rmt_pykih_338 awsui_tab-label_1acwa_dp0cl_7"><span>Badge</span></span>
                                                </button>
                                            </div>
                                        </li>
                                        <li class="awsui_tabs-tab_14rmt_pykih_329" role="presentation">
                                            <div class="awsui_tabs-tab-header-container_14rmt_pykih_349 awsui_tabs-tab-focusable_14rmt_pykih_497">
                                                <button class="awsui_tabs-tab-link_14rmt_pykih_410 awsui_tabs-tab-focusable_14rmt_pykih_497" aria-controls="awsui-tabs-12473-1733498994778-9458-third-panel" data-testid="third" id="awsui-tabs-12473-1733498994778-9458-third" aria-selected="false" role="tab" tabindex="-1" type="button"><span class="awsui_tabs-tab-label_14rmt_pykih_338 awsui_tab-label_1acwa_dp0cl_7"><span>Access Level</span></span>
                                                </button>
                                            </div>
                                        </li>
                                    </ul>
                                </div>
                            </div>
                            <div class="awsui_content_14iqq_zuudq_304">
                                <div class="awsui_content-inner_14iqq_zuudq_492 awsui_content-inner_1mwlm_oyjaq_5 awsui_with-header_14iqq_zuudq_499">
                                    <div class="awsui_tabs-container-content-wrapper_14rmt_pykih_577 awsui_with-paddings_14rmt_pykih_566">
                                        <div class="awsui_tabs-content_14rmt_pykih_542 awsui_tabs-content-active_14rmt_pykih_552" role="tabpanel" id="awsui-tabs-12473-1733498994778-9458-second-panel" tabindex="0" aria-labelledby="awsui-tabs-12473-1733498994778-9458-second">
                                            <div class="awsui_root_wih1l_1v07r_149 awsui_root_14iqq_zuudq_185 awsui_variant-default_14iqq_zuudq_229" data-selection-root="true" data-analytics-task-interaction-id="12563-1733498994808-2651">
                                                <div id="12566-1733498994808-2276" class="awsui_content-wrapper_14iqq_zuudq_304">
                                                    <div class="awsui_header_14iqq_zuudq_345 awsui_header_164jl_1ns0c_5">
                                                        <div>
                                                            <div class="awsui_header-controls_wih1l_1v07r_321 awsui_variant-container_wih1l_1v07r_215">
                                                                <div class="awsui_root_2qdw9_kiqfw_177 awsui_root-variant-h2_2qdw9_kiqfw_219">
                                                                    <div class="awsui_main_2qdw9_kiqfw_238">
                                                                        <div class="awsui_title_2qdw9_kiqfw_294 awsui_title-variant-h2_2qdw9_kiqfw_306">
                                                                            <h2 class="awsui_heading_2qdw9_kiqfw_370 awsui_heading-variant-h2_2qdw9_kiqfw_386"><span data-analytics-funnel-key="substep-name" class="awsui_heading-text_2qdw9_kiqfw_397 awsui_heading-text_105ke_268sp_5 awsui_heading-text-variant-h2_2qdw9_kiqfw_408" id="heading12568-1733498994808-3572">Badges</span><span class="awsui_counter_2qdw9_kiqfw_425"> (${profileData.Badge_Count || ''})</span></h2></div>
                                                                        <div class="awsui_actions_2qdw9_kiqfw_262 awsui_actions-variant-h2_2qdw9_kiqfw_274 awsui_actions-centered_2qdw9_kiqfw_267">
                                                                            <div class="awsui_root_18582_7onux_141 awsui_horizontal_18582_7onux_156 awsui_horizontal-xs_18582_7onux_166">
                                                                                <div class="awsui_child_18582_7onux_145">
                                                                                    <button class="awsui_button_vjswe_4v1qr_153 awsui_variant-normal_vjswe_4v1qr_204" data-analytics-funnel-value="button12598-1733498994828-9425" type="submit" data-analytics-performance-mark="12599-1733498994828-7252"><span class="awsui_content_vjswe_4v1qr_149 awsui_label_1f1d4_ocied_5">New Badge</span><span class="awsui_icon_vjswe_4v1qr_1159 awsui_icon-right_vjswe_4v1qr_1164 awsui_icon_h11ix_o4x4v_185 awsui_size-normal-mapped-height_h11ix_o4x4v_244 awsui_size-normal_h11ix_o4x4v_240 awsui_variant-normal_h11ix_o4x4v_316"><svg viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg" focusable="false" aria-hidden="true"><path d="M2.01 8h12M8 14l.01-12"></path></svg></span></button>
                                                                                </div>
                                                                                <div class="awsui_child_18582_7onux_145">
                                                                                    <button class="awsui_button_vjswe_4v1qr_153 awsui_variant-normal_vjswe_4v1qr_204 awsui_disabled_vjswe_4v1qr_289" data-analytics-funnel-value="button12601-1733498994828-5070" type="submit" disabled="" data-analytics-performance-mark="12602-1733498994828-5336"><span class="awsui_content_vjswe_4v1qr_149 awsui_label_1f1d4_ocied_5">Modify Badge</span><span class="awsui_icon_vjswe_4v1qr_1159 awsui_icon-right_vjswe_4v1qr_1164 awsui_icon_h11ix_o4x4v_185 awsui_size-normal-mapped-height_h11ix_o4x4v_244 awsui_size-normal_h11ix_o4x4v_240 awsui_variant-normal_h11ix_o4x4v_316"><svg viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg" focusable="false" aria-hidden="true"><path d="m6.19 13.275-4.19.7.7-4.19 7.2-7.2c.78-.78 2.05-.78 2.83 0l.66.66c.78.78.78 2.05 0 2.83l-7.2 7.2ZM9 3.995l3 3" class="stroke-linejoin-round"></path></svg></span></button>
                                                                                </div>
                                                                                <div class="awsui_child_18582_7onux_145">
                                                                                    <button class="awsui_button_vjswe_4v1qr_153 awsui_variant-normal_vjswe_4v1qr_204 awsui_disabled_vjswe_4v1qr_289" data-analytics-funnel-value="button12604-1733498994828-9552" type="submit" disabled="" data-analytics-performance-mark="12605-1733498994828-7586"><span class="awsui_content_vjswe_4v1qr_149 awsui_label_1f1d4_ocied_5">Delete Badge</span><span class="awsui_icon_vjswe_4v1qr_1159 awsui_icon-right_vjswe_4v1qr_1164 awsui_icon_h11ix_o4x4v_185 awsui_size-normal-mapped-height_h11ix_o4x4v_244 awsui_size-normal_h11ix_o4x4v_240 awsui_variant-normal_h11ix_o4x4v_316"><svg viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg" focusable="false" aria-hidden="true"><path d="m2 1.71 12 12M2 13.71l12-12" class="stroke-linejoin-round"></path></svg></span></button>
                                                                                </div>
                                                                                <div class="awsui_child_18582_7onux_145">
                                                                                    <button class="awsui_button_vjswe_4v1qr_153 awsui_variant-normal_vjswe_4v1qr_204 awsui_disabled_vjswe_4v1qr_289" data-analytics-funnel-value="button12607-1733498994828-2126" type="submit" disabled="" data-analytics-performance-mark="12608-1733498994828-6253"><span class="awsui_content_vjswe_4v1qr_149 awsui_label_1f1d4_ocied_5">Print Badge</span><span class="awsui_icon_vjswe_4v1qr_1159 awsui_icon-right_vjswe_4v1qr_1164 awsui_icon_h11ix_o4x4v_185 awsui_size-normal-mapped-height_h11ix_o4x4v_244 awsui_size-normal_h11ix_o4x4v_240 awsui_variant-normal_h11ix_o4x4v_316"><svg viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg" focusable="false" aria-hidden="true"><path d="M8 7c1.66 0 3-1.34 3-3S9.66 1 8 1 5 2.34 5 4s1.34 3 3 3Z"></path><path d="M2 16v-3c0-1.66 1.34-3 3-3h6c1.66 0 3 1.34 3 3v3" class="stroke-linejoin-round"></path></svg></span></button>
                                                                                </div>
                                                                            </div>
                                                                        </div>
                                                                    </div>
                                                                </div>
                                                                <div class="awsui_tools_wih1l_1v07r_160">
                                                                    <div class="awsui_tools-filtering_wih1l_1v07r_168">
                                                                        <div class="awsui_root_1sdq3_1brjz_141">
                                                                            <div class="awsui_input_1sdq3_1brjz_179 awsui_input-container_2rhyz_oflk9_309"><span class="awsui_input-icon-left_2rhyz_oflk9_314"><span class="awsui_icon_h11ix_o4x4v_185 awsui_size-normal-mapped-height_h11ix_o4x4v_244 awsui_size-normal_h11ix_o4x4v_240 awsui_variant-subtle_h11ix_o4x4v_325"><svg viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg" focusable="false" aria-hidden="true"><path d="m11 11 4 4M7 12A5 5 0 1 0 7 2a5 5 0 0 0 0 10Z" class="stroke-linejoin-round"></path></svg></span></span>
                                                                                <input aria-label="Filter report" class="awsui_input_2rhyz_oflk9_145 awsui_input-type-search_2rhyz_oflk9_286 awsui_input-has-icon-left_2rhyz_oflk9_271" autocomplete="off" type="search" value="">
                                                                            </div>
                                                                        </div>
                                                                    </div>
                                                                    <div class="awsui_tools-align-right_wih1l_1v07r_182">
                                                                        <div class="awsui_tools-pagination_wih1l_1v07r_186">
                                                                            <ul class="awsui_root_fvjdu_ioj3b_141">
                                                                                <li class="awsui_page-item_fvjdu_ioj3b_251">
                                                                                    <button class="awsui_arrow_fvjdu_ioj3b_218 awsui_button_fvjdu_ioj3b_184 awsui_button-disabled_fvjdu_ioj3b_213" type="button" aria-label="Previous page" disabled="" aria-current="false"><span class="awsui_icon_h11ix_o4x4v_185 awsui_size-normal-mapped-height_h11ix_o4x4v_244 awsui_size-normal_h11ix_o4x4v_240 awsui_variant-normal_h11ix_o4x4v_316 awsui_name-angle-left_h11ix_o4x4v_340"><svg viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg" focusable="false" aria-hidden="true"><path d="M11 2 5 8l6 6" class="stroke-linejoin-round"></path></svg></span></button>
                                                                                </li>
                                                                                <li class="awsui_page-item_fvjdu_ioj3b_251">
                                                                                    <button class="awsui_page-number_fvjdu_ioj3b_228 awsui_button_fvjdu_ioj3b_184 awsui_button-current_fvjdu_ioj3b_234" type="button" aria-label="Go to page 1" aria-current="true">1</button>
                                                                                </li>
                                                                                <li class="awsui_page-item_fvjdu_ioj3b_251">
                                                                                    <button class="awsui_arrow_fvjdu_ioj3b_218 awsui_button_fvjdu_ioj3b_184 awsui_button-disabled_fvjdu_ioj3b_213" type="button" aria-label="Next page" disabled="" aria-current="false"><span class="awsui_icon_h11ix_o4x4v_185 awsui_size-normal-mapped-height_h11ix_o4x4v_244 awsui_size-normal_h11ix_o4x4v_240 awsui_variant-normal_h11ix_o4x4v_316 awsui_name-angle-right_h11ix_o4x4v_342"><svg viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg" focusable="false" aria-hidden="true"><path d="m5 2 6 6-6 6" class="stroke-linejoin-round"></path></svg></span></button>
                                                                                </li>
                                                                            </ul>
                                                                        </div>
                                                                    </div>
                                                                </div>
                                                            </div>
                                                        </div>
                                                    </div>
                                                    <div class="awsui_content_14iqq_zuudq_304">
                                                        <div class="awsui_content-inner_14iqq_zuudq_492 awsui_content-inner_1mwlm_oyjaq_5 awsui_with-header_14iqq_zuudq_499">
                                                            <div class="awsui_wrapper_wih1l_1v07r_208 awsui_variant-container_wih1l_1v07r_215 awsui_has-header_wih1l_1v07r_221" style="scroll-padding-inline: 384px 0px;" role="region" tabindex="0" aria-labelledby="heading12568-1733498994808-3572">
                                                                <div class="awsui_wrapper-content-measure_wih1l_1v07r_215"></div>
                                                                ${BadgeData}
                                                                <span class="awsui_tracker_x7peu_12e0g_249"></span></div>
                                                            <div class="awsui_sticky-scrollbar_faqt8_1we8w_177 awsui_sticky-scrollbar-offset_faqt8_1we8w_195 awsui_sticky-scrollbar-visible_faqt8_1we8w_189" style="block-size: 17px; inline-size: 1463px; inset-block-end: var(--awsui-sticky-vertical-bottom-offset, 0px);">
                                                                <div class="awsui_sticky-scrollbar-content_faqt8_1we8w_186" style="block-size: 17px; inline-size: 1984px;"></div>
                                                            </div>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                        <div class="awsui_tabs-content_14rmt_pykih_542" role="tabpanel" id="awsui-tabs-12473-1733498994778-9458-third-panel" tabindex="0" aria-labelledby="awsui-tabs-12473-1733498994778-9458-third"></div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="awsui_child_18582_7onux_145"></div>
                <div class="awsui_child_18582_7onux_145"></div>
            </div>
        `;

        enableSorting()
    }

    function generateBadgeTableHTML(profileData) {
        if (!profileData || !profileData.Badges) {
            console.error('Invalid profileData.');
            return '';
        }

        // Build the table structure dynamically
        const badgeRows = profileData.Badges.map((badge, index) => `
            <tr class="awsui_row_wih1l_1v07r_356" aria-rowindex="${index + 2}">
                <td class="awsui_body-cell_c6tup_et2x0_148 awsui_body-cell-first-row_c6tup_et2x0_787 awsui_selection-control_wih1l_1v07r_279 awsui_has-selection_c6tup_et2x0_445 awsui_sticky-cell_c6tup_et2x0_445" style="inset-inline-start: 0px;">
                    <div class="awsui_body-cell-content_c6tup_et2x0_156">
                        <label for="7163-1733753662273-581" class="awsui_label_1s55x_1iiee_145 awsui_root_1s55x_1iiee_141"><span class="awsui_wrapper_1wepg_1vmnx_162 awsui_radio_1mabk_i06od_177"><span class="awsui_label-wrapper_1wepg_1vmnx_168"><span class="awsui_control_1wepg_1vmnx_202 awsui_radio-control_1mabk_i06od_189"><svg viewBox="0 0 100 100" focusable="false" aria-hidden="true"><circle class="awsui_styled-circle-border_1mabk_i06od_219" stroke-width="8" cx="50" cy="50" r="46"></circle><circle class="awsui_styled-circle-fill_1mabk_i06od_228" stroke-width="30" cx="50" cy="50" r="35"></circle></svg><input id="7163-1733753662273-581" class="awsui_native-input_1wepg_1vmnx_158 awsui_native-input_13tpe_9w8pd_6" type="radio" name="6909-1733753661511-1843" value=""><span class="awsui_outline_1wepg_1vmnx_151 awsui_outline_1mabk_i06od_197"></span></span><span class="awsui_content_1wepg_1vmnx_141 awsui_empty-content_1wepg_1vmnx_179"></span></span>
                            </span>
                        </label><span class="awsui_stud_1s55x_1iiee_159" aria-hidden="true">&nbsp;</span>
                    </div>
                </td>
                <td class="awsui_body-cell_c6tup_et2x0_148">
                    <div class="awsui_body-cell-content_c6tup_et2x0_156">${badge.Badge_ID || ''}</div>
                </td>
                <td class="awsui_body-cell_c6tup_et2x0_148">
                    <div class="awsui_body-cell-content_c6tup_et2x0_156">
                        <span class="awsui_badge_1yjyg_1816x_141 awsui_badge-color-${badge.Badge_Status === 'Active' ? 'green_1yjyg_1816x_190' : 'blue_1yjyg_1816x_193'}">${badge.Badge_Status || ''}</span>
                    </div>
                </td>
                <td class="awsui_body-cell_c6tup_et2x0_148">
                    <div class="awsui_body-cell-content_c6tup_et2x0_156">${badge.Badge_Type || ''}</div>
                </td>
                <td class="awsui_body-cell_c6tup_et2x0_148">
                    <div class="awsui_body-cell-content_c6tup_et2x0_156">${badge.Badge_ActivateOn || ''}</div>
                </td>
                <td class="awsui_body-cell_c6tup_et2x0_148">
                    <div class="awsui_body-cell-content_c6tup_et2x0_156">${badge.Badge_DeactivateOn || ''}</div>
                </td>
                <td class="awsui_body-cell_c6tup_et2x0_148">
                    <div class="awsui_body-cell-content_c6tup_et2x0_156">${badge.Badge_LastUpdatedUTC || ''}</div>
                </td>
                <td class="awsui_body-cell_c6tup_et2x0_148">
                    <div class="awsui_body-cell-content_c6tup_et2x0_156">${badge.Badge_LastLocationReaderName || ''}</div>
                </td>
                <td class="awsui_body-cell_c6tup_et2x0_148">
                    <div class="awsui_body-cell-content_c6tup_et2x0_156">${badge.Badge_LastUpdatedUTC || ''}</div>
                </td>
                <td class="awsui_body-cell_c6tup_et2x0_148">
                    <div class="awsui_body-cell-content_c6tup_et2x0_156">${badge.Badge_LastLocationEventType || ''}</div>
                </td>
            </tr>
        `).join('');

        const badgeHeader = `
            <tr data-selection-item="all" aria-rowindex="1">
                <th data-focus-id="header-Symbol(selection-column-id)" class="awsui_header-cell_1spae_13mz6_145 awsui_selection-control_wih1l_1v07r_279 awsui_selection-control-header_wih1l_1v07r_286 awsui_sticky-cell_1spae_13mz6_215" scope="col" style="inset-inline-start: 0px;"><span class="awsui_root_xttbq_1ekiv_141"></span><span class="awsui_divider_x7peu_12e0g_146 awsui_divider-disabled_x7peu_12e0g_160"></span></th>
                <th data-focus-id="header-badgeID" class="awsui_header-cell_1spae_13mz6_145 awsui_header-cell-sortable_1spae_13mz6_212 awsui_sticky-cell_1spae_13mz6_215" scope="col" aria-sort="none" style="width: 150px; min-width: 120px; inset-inline-start: 54px;">
                    <div data-focus-id="sorting-control-badgeID" class="awsui_header-cell-content_1spae_13mz6_272" tabindex="0" role="button">
                        <div class="awsui_header-cell-text_1spae_13mz6_344 awsui_header-cell-text_dpuyq_1id1o_5" id="table-header-2460-1733517192642-9109">Badge ID</div><span class="awsui_sorting-icon_1spae_13mz6_258"><span class="awsui_icon_h11ix_o4x4v_185 awsui_size-normal-mapped-height_h11ix_o4x4v_244 awsui_size-normal_h11ix_o4x4v_240 awsui_variant-normal_h11ix_o4x4v_316"><svg viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg" focusable="false" aria-hidden="true"><path d="m8 11 4-6H4l4 6Z" class="stroke-linejoin-round"></path></svg></span></span>
                    </div>
                    <button class="awsui_resizer_x7peu_12e0g_167" aria-labelledby="table-header-2460-1733517192642-9109" tabindex="0" data-focus-id="resize-control-badgeID"></button><span class="awsui_divider_x7peu_12e0g_146" data-awsui-table-suppress-navigation="true" id="2461-1733517192642-1974" role="separator" tabindex="-1" aria-hidden="true" aria-orientation="vertical" aria-valuenow="150" aria-valuetext="150" aria-valuemin="120" data-focus-id="resize-control-badgeID"></span></th>
                <th data-focus-id="header-badgeStatus" class="awsui_header-cell_1spae_13mz6_145 awsui_header-cell-sortable_1spae_13mz6_212 awsui_header-cell-sorted_1spae_13mz6_330 awsui_header-cell-ascending_1spae_13mz6_354 awsui_sticky-cell_1spae_13mz6_215" scope="col" aria-sort="ascending" style="width: 180px; min-width: 150px; inset-inline-start: 204px;">
                    <div data-focus-id="sorting-control-badgeStatus" class="awsui_header-cell-content_1spae_13mz6_272" tabindex="0" role="button">
                        <div class="awsui_header-cell-text_1spae_13mz6_344 awsui_header-cell-text_dpuyq_1id1o_5" id="table-header-2462-1733517192642-4238">Status</div><span class="awsui_sorting-icon_1spae_13mz6_258"><span class="awsui_icon_h11ix_o4x4v_185 awsui_size-normal-mapped-height_h11ix_o4x4v_244 awsui_size-normal_h11ix_o4x4v_240 awsui_variant-normal_h11ix_o4x4v_316"><svg viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg" focusable="false" aria-hidden="true"><path d="m8 5 4 6H4l4-6Z" class="filled stroke-linejoin-round"></path></svg></span></span>
                    </div>
                    <button class="awsui_resizer_x7peu_12e0g_167" aria-labelledby="table-header-2462-1733517192642-4238" tabindex="0" data-focus-id="resize-control-badgeStatus"></button><span class="awsui_divider_x7peu_12e0g_146" data-awsui-table-suppress-navigation="true" id="2463-1733517192642-808" role="separator" tabindex="-1" aria-hidden="true" aria-orientation="vertical" aria-valuenow="180" aria-valuetext="180" aria-valuemin="150" data-focus-id="resize-control-badgeStatus"></span></th>
                <th data-focus-id="header-badgeType" class="awsui_header-cell_1spae_13mz6_145 awsui_header-cell-sortable_1spae_13mz6_212" scope="col" aria-sort="none" style="width: 180px; min-width: 150px;">
                    <div data-focus-id="sorting-control-badgeType" class="awsui_header-cell-content_1spae_13mz6_272" tabindex="0" role="button">
                        <div class="awsui_header-cell-text_1spae_13mz6_344 awsui_header-cell-text_dpuyq_1id1o_5" id="table-header-2464-1733517192642-2336">Type</div><span class="awsui_sorting-icon_1spae_13mz6_258"><span class="awsui_icon_h11ix_o4x4v_185 awsui_size-normal-mapped-height_h11ix_o4x4v_244 awsui_size-normal_h11ix_o4x4v_240 awsui_variant-normal_h11ix_o4x4v_316"><svg viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg" focusable="false" aria-hidden="true"><path d="m8 11 4-6H4l4 6Z" class="stroke-linejoin-round"></path></svg></span></span>
                    </div>
                    <button class="awsui_resizer_x7peu_12e0g_167" aria-labelledby="table-header-2464-1733517192642-2336" tabindex="0" data-focus-id="resize-control-badgeType"></button><span class="awsui_divider_x7peu_12e0g_146" data-awsui-table-suppress-navigation="true" id="2465-1733517192643-2570" role="separator" tabindex="-1" aria-hidden="true" aria-orientation="vertical" aria-valuenow="180" aria-valuetext="180" aria-valuemin="150" data-focus-id="resize-control-badgeType"></span></th>
                <th data-focus-id="header-badgeActive" class="awsui_header-cell_1spae_13mz6_145 awsui_header-cell-sortable_1spae_13mz6_212" scope="col" aria-sort="none" style="width: 220px; min-width: 180px;">
                    <div data-focus-id="sorting-control-badgeActive" class="awsui_header-cell-content_1spae_13mz6_272" tabindex="0" role="button">
                        <div class="awsui_header-cell-text_1spae_13mz6_344 awsui_header-cell-text_dpuyq_1id1o_5" id="table-header-2466-1733517192643-2830">Activate On</div><span class="awsui_sorting-icon_1spae_13mz6_258"><span class="awsui_icon_h11ix_o4x4v_185 awsui_size-normal-mapped-height_h11ix_o4x4v_244 awsui_size-normal_h11ix_o4x4v_240 awsui_variant-normal_h11ix_o4x4v_316"><svg viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg" focusable="false" aria-hidden="true"><path d="m8 11 4-6H4l4 6Z" class="stroke-linejoin-round"></path></svg></span></span>
                    </div>
                    <button class="awsui_resizer_x7peu_12e0g_167" aria-labelledby="table-header-2466-1733517192643-2830" tabindex="0" data-focus-id="resize-control-badgeActive"></button><span class="awsui_divider_x7peu_12e0g_146" data-awsui-table-suppress-navigation="true" id="2467-1733517192643-2642" role="separator" tabindex="-1" aria-hidden="true" aria-orientation="vertical" aria-valuenow="220" aria-valuetext="220" aria-valuemin="180" data-focus-id="resize-control-badgeActive"></span></th>
                <th data-focus-id="header-badgeDeactivate" class="awsui_header-cell_1spae_13mz6_145 awsui_header-cell-sortable_1spae_13mz6_212" scope="col" aria-sort="none" style="width: 230px; min-width: 180px;">
                    <div data-focus-id="sorting-control-badgeDeactivate" class="awsui_header-cell-content_1spae_13mz6_272" tabindex="0" role="button">
                        <div class="awsui_header-cell-text_1spae_13mz6_344 awsui_header-cell-text_dpuyq_1id1o_5" id="table-header-2468-1733517192643-4818">Deactivate On</div><span class="awsui_sorting-icon_1spae_13mz6_258"><span class="awsui_icon_h11ix_o4x4v_185 awsui_size-normal-mapped-height_h11ix_o4x4v_244 awsui_size-normal_h11ix_o4x4v_240 awsui_variant-normal_h11ix_o4x4v_316"><svg viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg" focusable="false" aria-hidden="true"><path d="m8 11 4-6H4l4 6Z" class="stroke-linejoin-round"></path></svg></span></span>
                    </div>
                    <button class="awsui_resizer_x7peu_12e0g_167" aria-labelledby="table-header-2468-1733517192643-4818" tabindex="0" data-focus-id="resize-control-badgeDeactivate"></button><span class="awsui_divider_x7peu_12e0g_146" data-awsui-table-suppress-navigation="true" id="2469-1733517192643-9842" role="separator" tabindex="-1" aria-hidden="true" aria-orientation="vertical" aria-valuenow="230" aria-valuetext="230" aria-valuemin="180" data-focus-id="resize-control-badgeDeactivate"></span></th>
                <th data-focus-id="header-badgeLastChanged" class="awsui_header-cell_1spae_13mz6_145 awsui_header-cell-sortable_1spae_13mz6_212" scope="col" aria-sort="none" style="width: 230px; min-width: 180px;">
                    <div data-focus-id="sorting-control-badgeLastChanged" class="awsui_header-cell-content_1spae_13mz6_272" tabindex="0" role="button">
                        <div class="awsui_header-cell-text_1spae_13mz6_344 awsui_header-cell-text_dpuyq_1id1o_5" id="table-header-2470-1733517192643-2802">Badge Last Updated UTC</div><span class="awsui_sorting-icon_1spae_13mz6_258"><span class="awsui_icon_h11ix_o4x4v_185 awsui_size-normal-mapped-height_h11ix_o4x4v_244 awsui_size-normal_h11ix_o4x4v_240 awsui_variant-normal_h11ix_o4x4v_316"><svg viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg" focusable="false" aria-hidden="true"><path d="m8 11 4-6H4l4 6Z" class="stroke-linejoin-round"></path></svg></span></span>
                    </div>
                    <button class="awsui_resizer_x7peu_12e0g_167" aria-labelledby="table-header-2470-1733517192643-2802" tabindex="0" data-focus-id="resize-control-badgeLastChanged"></button><span class="awsui_divider_x7peu_12e0g_146" data-awsui-table-suppress-navigation="true" id="2471-1733517192644-1995" role="separator" tabindex="-1" aria-hidden="true" aria-orientation="vertical" aria-valuenow="230" aria-valuetext="230" aria-valuemin="180" data-focus-id="resize-control-badgeLastChanged"></span></th>
                <th data-focus-id="header-lastLocationReaderName" class="awsui_header-cell_1spae_13mz6_145 awsui_header-cell-sortable_1spae_13mz6_212" scope="col" aria-sort="none" style="width: 250px; min-width: 180px;">
                    <div data-focus-id="sorting-control-lastLocationReaderName" class="awsui_header-cell-content_1spae_13mz6_272" tabindex="0" role="button">
                        <div class="awsui_header-cell-text_1spae_13mz6_344 awsui_header-cell-text_dpuyq_1id1o_5" id="table-header-2472-1733517192644-8928">Last Location Reader Name</div><span class="awsui_sorting-icon_1spae_13mz6_258"><span class="awsui_icon_h11ix_o4x4v_185 awsui_size-normal-mapped-height_h11ix_o4x4v_244 awsui_size-normal_h11ix_o4x4v_240 awsui_variant-normal_h11ix_o4x4v_316"><svg viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg" focusable="false" aria-hidden="true"><path d="m8 11 4-6H4l4 6Z" class="stroke-linejoin-round"></path></svg></span></span>
                    </div>
                    <button class="awsui_resizer_x7peu_12e0g_167" aria-labelledby="table-header-2472-1733517192644-8928" tabindex="0" data-focus-id="resize-control-lastLocationReaderName"></button><span class="awsui_divider_x7peu_12e0g_146" data-awsui-table-suppress-navigation="true" id="2473-1733517192644-2547" role="separator" tabindex="-1" aria-hidden="true" aria-orientation="vertical" aria-valuenow="250" aria-valuetext="250" aria-valuemin="180" data-focus-id="resize-control-lastLocationReaderName"></span></th>
                <th data-focus-id="header-lastLocationTimestamp" class="awsui_header-cell_1spae_13mz6_145 awsui_header-cell-sortable_1spae_13mz6_212" scope="col" aria-sort="none" style="width: 260px; min-width: 180px;">
                    <div data-focus-id="sorting-control-lastLocationTimestamp" class="awsui_header-cell-content_1spae_13mz6_272" tabindex="0" role="button">
                        <div class="awsui_header-cell-text_1spae_13mz6_344 awsui_header-cell-text_dpuyq_1id1o_5" id="table-header-2474-1733517192644-688">Last Location Timestamp UTC</div><span class="awsui_sorting-icon_1spae_13mz6_258"><span class="awsui_icon_h11ix_o4x4v_185 awsui_size-normal-mapped-height_h11ix_o4x4v_244 awsui_size-normal_h11ix_o4x4v_240 awsui_variant-normal_h11ix_o4x4v_316"><svg viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg" focusable="false" aria-hidden="true"><path d="m8 11 4-6H4l4 6Z" class="stroke-linejoin-round"></path></svg></span></span>
                    </div>
                    <button class="awsui_resizer_x7peu_12e0g_167" aria-labelledby="table-header-2474-1733517192644-688" tabindex="0" data-focus-id="resize-control-lastLocationTimestamp"></button><span class="awsui_divider_x7peu_12e0g_146" data-awsui-table-suppress-navigation="true" id="2475-1733517192644-2841" role="separator" tabindex="-1" aria-hidden="true" aria-orientation="vertical" aria-valuenow="260" aria-valuetext="260" aria-valuemin="180" data-focus-id="resize-control-lastLocationTimestamp"></span></th>
                <th data-focus-id="header-lastLocationEventType" class="awsui_header-cell_1spae_13mz6_145 awsui_header-cell-sortable_1spae_13mz6_212" scope="col" aria-sort="none" style="width: 230px; min-width: 180px;">
                    <div data-focus-id="sorting-control-lastLocationEventType" class="awsui_header-cell-content_1spae_13mz6_272" tabindex="0" role="button">
                        <div class="awsui_header-cell-text_1spae_13mz6_344 awsui_header-cell-text_dpuyq_1id1o_5" id="table-header-2476-1733517192644-2589">Last Location Event Type</div><span class="awsui_sorting-icon_1spae_13mz6_258"><span class="awsui_icon_h11ix_o4x4v_185 awsui_size-normal-mapped-height_h11ix_o4x4v_244 awsui_size-normal_h11ix_o4x4v_240 awsui_variant-normal_h11ix_o4x4v_316"><svg viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg" focusable="false" aria-hidden="true"><path d="m8 11 4-6H4l4 6Z" class="stroke-linejoin-round"></path></svg></span></span>
                    </div>
                    <button class="awsui_resizer_x7peu_12e0g_167" aria-labelledby="table-header-2476-1733517192644-2589" tabindex="0" data-focus-id="resize-control-lastLocationEventType"></button><span class="awsui_divider_x7peu_12e0g_146" data-awsui-table-suppress-navigation="true" id="2477-1733517192644-4733" role="separator" tabindex="-1" aria-hidden="true" aria-orientation="vertical" aria-valuenow="230" aria-valuetext="230" aria-valuemin="180" data-focus-id="resize-control-lastLocationEventType"></span></th>
            </tr>
            `;

        // Combine the table header, rows, and footer
        return `
            <table class="awsui_table_wih1l_1v07r_198 awsui_table-layout-fixed_wih1l_1v07r_204" aria-rowcount="${profileData.Badges.length + 1}">
                <thead class="awsui_thead-active_wih1l_1v07r_355">
                    ${badgeHeader}
                </thead>
                <tbody>
                    ${badgeRows}
                </tbody>
            </table>
        `;
    }

    function enableSorting() {
        const table = document.querySelector('.awsui_table_wih1l_1v07r_198.awsui_table-layout-fixed_wih1l_1v07r_204');
    
        if (!table) {
            console.error('Table not found!');
            return;
        }
    
        const headers = table.querySelectorAll('thead tr th');
    
        headers.forEach((header) => {
            header.addEventListener('click', () => {
                const currentSort = header.getAttribute('aria-sort') || 'none';
    
                // Reset all headers
                headers.forEach((hdr) => {
                    hdr.setAttribute('aria-sort', 'none');
                    hdr.classList.remove('awsui_header-cell-ascending', 'awsui_header-cell-descending');
                    resetSortingIcon(hdr);
                });
    
                // Determine the next sorting state
                let nextSort;
                if (currentSort === 'none') {
                    nextSort = 'ascending';
                } else if (currentSort === 'ascending') {
                    nextSort = 'descending';
                } else {
                    nextSort = 'none';
                }
    
                // Update the clicked header
                if (nextSort !== 'none') {
                    header.setAttribute('aria-sort', nextSort);
                    header.classList.add(
                        nextSort === 'ascending' ? 'awsui_header-cell-ascending' : 'awsui_header-cell-descending'
                    );
                    updateSortingIcon(header, nextSort);
                }
    
                // Sort rows if ascending or descending
                if (nextSort !== 'none') {
                    sortTableRows(table, header.cellIndex, nextSort);
                }
            });
        });
    }
    
    function resetSortingIcon(header) {
        const icon = header.querySelector('.awsui_sorting-icon_1spae_13mz6_258 svg path');
        if (icon) {
            icon.setAttribute('d', ''); // Reset icon to default (or empty path)
        }
    }
    
    function updateSortingIcon(header, direction) {
        const icon = header.querySelector('.awsui_sorting-icon_1spae_13mz6_258 svg path');
        if (icon) {
            if (direction === 'ascending') {
                icon.setAttribute('d', 'm8 5 4 6H4l4-6Z'); // Upward arrow
            } else if (direction === 'descending') {
                icon.setAttribute('d', 'm8 11 4-6H4l4 6Z'); // Downward arrow
            }
        }
    }
    
    function sortTableRows(table, columnIndex, direction) {
        const rows = Array.from(table.querySelectorAll('tbody tr'));
        const isNumeric = !isNaN(parseFloat(rows[0].children[columnIndex].textContent.trim()));
    
        // Sort rows
        rows.sort((a, b) => {
            const aText = a.children[columnIndex].textContent.trim();
            const bText = b.children[columnIndex].textContent.trim();
    
            if (isNumeric) {
                return direction === 'ascending'
                    ? parseFloat(aText) - parseFloat(bText)
                    : parseFloat(bText) - parseFloat(aText);
            } else {
                return direction === 'ascending'
                    ? aText.localeCompare(bText)
                    : bText.localeCompare(aText);
            }
        });
    
        // Re-append sorted rows to the table body
        const tbody = table.querySelector('tbody');
        rows.forEach((row) => tbody.appendChild(row));
    }
    

    /*function enableSorting() {
        const table = document.querySelector('.awsui_table_wih1l_1v07r_198.awsui_table-layout-fixed_wih1l_1v07r_204'); // Get the table element
        const headers = table.querySelectorAll('thead tr td'); // Get all column headers
        
        headers.forEach((header, index) => {
            header.addEventListener('click', () => {
                const isAscending = header.classList.contains('ascending');
                const rows = Array.from(table.querySelectorAll('tbody tr')); // Get all rows
                
                // Sort the rows based on the clicked column
                const sortedRows = rows.sort((rowA, rowB) => {
                    const cellA = rowA.querySelectorAll('td')[index].textContent.trim();
                    const cellB = rowB.querySelectorAll('td')[index].textContent.trim();
    
                    // For date columns, compare as dates
                    if (index === 5 || index === 6) { // LastUpdatedUTC or DeactivateOn (date columns)
                        return isAscending
                            ? new Date(cellA) - new Date(cellB)
                            : new Date(cellB) - new Date(cellA);
                    }
                    
                    // For text or numeric columns, compare alphabetically
                    return isAscending
                        ? cellA.localeCompare(cellB)
                        : cellB.localeCompare(cellA);
                });
    
                // Clear existing rows and append sorted rows
                table.querySelector('tbody').innerHTML = ''; // Clear the existing rows
                table.querySelector('tbody').append(...sortedRows); // Append sorted rows
    
                // Toggle sorting classes for the headers
                headers.forEach(h => h.classList.remove('ascending', 'descending'));
                header.classList.toggle('ascending', !isAscending);
                header.classList.toggle('descending', isAscending);
            });
        });
    }*/

    // Button click event listener
    searchButton.addEventListener('click', function (event) {
        event.preventDefault(); // Prevent form submission
        performSearch();
    });

    // Enter key event listeners for both inputs
    idInputField.addEventListener('keypress', function (event) {
        if (event.key === "Enter") {
            event.preventDefault();
            performSearch();
        }
    });

    loginInputField.addEventListener('keypress', function (event) {
        if (event.key === "Enter") {
            event.preventDefault();
            performSearch();
        }
    });
});

<th data-focus-id="header-badgeStatus" class="awsui_header-cell_1spae_13mz6_145 awsui_header-cell-sortable_1spae_13mz6_212 awsui_header-cell-sorted_1spae_13mz6_330 awsui_header-cell-ascending_1spae_13mz6_354 awsui_sticky-cell_1spae_13mz6_215" scope="col" aria-sort="ascending" style="width: 180px; min-width: 150px; inset-inline-start: 204px;">
    <div data-focus-id="sorting-control-badgeStatus" class="awsui_header-cell-content_1spae_13mz6_272" tabindex="0" role="button">
        <div class="awsui_header-cell-text_1spae_13mz6_344 awsui_header-cell-text_dpuyq_1id1o_5" id="table-header-2462-1733517192642-4238">Status</div><span class="awsui_sorting-icon_1spae_13mz6_258"><span class="awsui_icon_h11ix_o4x4v_185 awsui_size-normal-mapped-height_h11ix_o4x4v_244 awsui_size-normal_h11ix_o4x4v_240 awsui_variant-normal_h11ix_o4x4v_316"><svg viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg" focusable="false" aria-hidden="true"><path d="m8 5 4 6H4l4-6Z" class="filled stroke-linejoin-round"></path></svg></span></span>
    </div>
    <button class="awsui_resizer_x7peu_12e0g_167" aria-labelledby="table-header-2462-1733517192642-4238" tabindex="0" data-focus-id="resize-control-badgeStatus"></button><span class="awsui_divider_x7peu_12e0g_146" data-awsui-table-suppress-navigation="true" id="2463-1733517192642-808" role="separator" tabindex="-1" aria-hidden="true" aria-orientation="vertical" aria-valuenow="180" aria-valuetext="180" aria-valuemin="150" data-focus-id="resize-control-badgeStatus"></span>
</th>;

<th data-focus-id="header-badgeStatus" class="awsui_header-cell_1spae_13mz6_145 awsui_header-cell-sortable_1spae_13mz6_212 awsui_header-cell-sorted_1spae_13mz6_330 awsui_header-cell-descending_1spae_13mz6_355 awsui_sticky-cell_1spae_13mz6_215" scope="col" aria-sort="descending" style="width: 180px; min-width: 150px; inset-inline-start: 204px;">
    <div data-focus-id="sorting-control-badgeStatus" class="awsui_header-cell-content_1spae_13mz6_272" tabindex="0" role="button">
        <div class="awsui_header-cell-text_1spae_13mz6_344 awsui_header-cell-text_dpuyq_1id1o_5" id="table-header-8705-1733758535424-3908">Status</div><span class="awsui_sorting-icon_1spae_13mz6_258"><span class="awsui_icon_h11ix_o4x4v_185 awsui_size-normal-mapped-height_h11ix_o4x4v_244 awsui_size-normal_h11ix_o4x4v_240 awsui_variant-normal_h11ix_o4x4v_316"><svg viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg" focusable="false" aria-hidden="true"><path d="m8 11 4-6H4l4 6Z" class="filled stroke-linejoin-round"></path></svg></span></span>
    </div>
    <button class="awsui_resizer_x7peu_12e0g_167" aria-labelledby="table-header-8705-1733758535424-3908" tabindex="0" data-focus-id="resize-control-badgeStatus"></button><span class="awsui_divider_x7peu_12e0g_146" data-awsui-table-suppress-navigation="true" id="8706-1733758535424-2527" role="separator" tabindex="-1" aria-hidden="true" aria-orientation="vertical" aria-valuenow="180" aria-valuetext="180" aria-valuemin="150" data-focus-id="resize-control-badgeStatus"></span>
</th>;

<th data-focus-id="header-badgeType" class="awsui_header-cell_1spae_13mz6_145 awsui_header-cell-sortable_1spae_13mz6_212" scope="col" aria-sort="none" style="width: 180px; min-width: 150px;">
    <div data-focus-id="sorting-control-badgeType" class="awsui_header-cell-content_1spae_13mz6_272" tabindex="0" role="button">
        <div class="awsui_header-cell-text_1spae_13mz6_344 awsui_header-cell-text_dpuyq_1id1o_5" id="table-header-2464-1733517192642-2336">Type</div><span class="awsui_sorting-icon_1spae_13mz6_258"><span class="awsui_icon_h11ix_o4x4v_185 awsui_size-normal-mapped-height_h11ix_o4x4v_244 awsui_size-normal_h11ix_o4x4v_240 awsui_variant-normal_h11ix_o4x4v_316"><svg viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg" focusable="false" aria-hidden="true"><path d="m8 11 4-6H4l4 6Z" class="stroke-linejoin-round"></path></svg></span></span>
    </div>
    <button class="awsui_resizer_x7peu_12e0g_167" aria-labelledby="table-header-2464-1733517192642-2336" tabindex="0" data-focus-id="resize-control-badgeType"></button><span class="awsui_divider_x7peu_12e0g_146" data-awsui-table-suppress-navigation="true" id="2465-1733517192643-2570" role="separator" tabindex="-1" aria-hidden="true" aria-orientation="vertical" aria-valuenow="180" aria-valuetext="180" aria-valuemin="150" data-focus-id="resize-control-badgeType"></span>
</th>;